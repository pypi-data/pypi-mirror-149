# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime
from typing import List, Optional

from aiokafka import AIOKafkaProducer
from kafka.errors import UnknownTopicOrPartitionError, KafkaTimeoutError
from patchwork.core import AsyncPublisher, Task
from pydantic import validator, root_validator

from .common import MissingTopicBehaviour, CompressionType, AckPolicy, create_topics, get_node_id, SECOND


class AsyncKafkaPublisher(AsyncPublisher):

    class Config(AsyncPublisher.Config):
        """
        Kafka asynchronous publisher settings

        :cvar kafka_hosts:
            A comma separated hostnames with optional port number of bootstrap kafka brokers.
            Example: ```hostname1.mydomain,hostname2.mydomain:4000```
        :cvar missing_topic:  Behaviour of producer when topic is missing
        :cvar default_partitions_count:
            If missing behaviour is to create a topic tells how many partitions should be created
        :cvar default_replication_factor:
            If missing behaviour is to create a topic tells what replication factor new topic should have
        :cvar compression_type:
            If missing behaviour is to create a topic tells what compression type new topic should have
        :cvar request_timeout_ms: Default timeout for all requests to Kafka brokers (in miliseconds)
        :cvar ack_policy:
            Setup producer ACK (acknowledges) policy
        :cvar default_topic:
            Set default topic for all tasks which don't have `queue_name` specified in their metadata
        :cvar postpone_queue_name:
            Kafka does not support postponed messages, so to avoid re-taking them all time until not_before time,
            producer may put postponed messages to the special queue which handles messages rolling and re-sending
            to destination queue when their time comes up (see Patchwork Kafka Scheduler package)
        """
        kafka_hosts: List[str]
        missing_topic: MissingTopicBehaviour = MissingTopicBehaviour.ERROR
        default_partitions_count: Optional[int]
        default_replication_factor: Optional[int]
        compression_type: CompressionType = CompressionType.NONE
        request_timeout_ms: int = 30*SECOND
        ack_policy: AckPolicy = AckPolicy.ACK_ALL
        default_topic: str = None
        postpone_queue_name: str = None

        @validator('default_partitions_count')
        def validate_dpc(cls, v):
            if v is not None and v <= 0:
                raise ValueError("default_partitions_count must be a positive number")
            return v

        @validator('default_replication_factor')
        def validate_drf(cls, v):
            if v is not None and v <= 0:
                raise ValueError("default_replication_factor must be a positive number")
            return v

        @validator('request_timeout_ms')
        def validate_rtm(cls, v):
            if v <= 0:
                raise ValueError("request_timeout_ms must be a positive number")
            return v

        @root_validator(pre=True)
        def validate_topic_creation(cls, values):
            if values.get('missing_topic') == MissingTopicBehaviour.CREATE:
                if values.get('default_partitions_count') is None:
                    raise ValueError("default_partitions_count must be specified for missing_topic_behaviour=CREATE")
                if values.get('default_replication_factor') is None:
                    raise ValueError("default_replication_factor must be specified for missing_topic_behaviour=CREATE")
            return values

    _producer: AIOKafkaProducer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.settings.missing_topic == MissingTopicBehaviour.ERROR:
            self.missing_topic_handler = self.mtb_error
        elif self.settings.missing_topic == MissingTopicBehaviour.SKIP:
            self.missing_topic_handler = self.mtb_skip
        elif self.settings.missing_topic == MissingTopicBehaviour.CREATE:
            self.missing_topic_handler = self.mtb_create
        else:
            raise ValueError(f'unsupported missing topic behaviour: {self.settings.missing_topic_behaviour}')

        self._producer_lock = asyncio.Lock()
        self.loop = asyncio.get_event_loop()

    def __repr__(self):
        res = super().__repr__()
        return f"<{res[1:-1]} [brokers={','.join(self.settings.kafka_hosts)}]>"

    async def _start(self):
        """
        Starts the producer
        :return:
        """
        await self._start_producer()

    async def _stop(self):
        """
        Stops the producer
        :return:
        """
        try:
            await self._producer.flush()
            await self._producer.stop()
        except Exception as e:
            self.logger.exception(f"stopping kafka producer failed {e.__class__.__name__}({e})")

        self.logger.debug("kafka producer stopped")

    def _prepare_task(self, task: Task) -> bytes:
        if not task.meta.queue_name and self.settings.default_topic is None:
            raise ValueError('neither task queue name nor default_topic on kafka publisher given')

        payload = super()._prepare_task(task)
        return payload

    async def _send(self, payload: bytes, task: Task, timeout: float = None):
        topic_name = task.meta.queue_name
        if task.meta.HasField('not_before') and \
                task.meta.not_before.ToDatetime() < datetime.now() and \
                self.settings.postpone_queue_name:
            # put postponed tasks on the special queue, don't change task meta
            topic_name = self.settings.postpone_queue_name

        # following metadata send as task headers on Kafka so it will be accessible without
        # parsing the task, might be useful on receiver side to filter messages faster,
        # or for debug purposes
        headers = [
            ('id', task.uuid.encode()),
            ('queue_name', task.meta.queue_name.encode()),
        ]

        if task.meta.HasField('not_before'):
            headers.append(('not_before', task.meta.not_bfore.ToSeconds().to_bytes(8, byteorder='big')))

        if task.meta.HasField('expires'):
            headers.append(('expires', task.meta.expires.ToSeconds().to_bytes(8, byteorder='big')))

        if not topic_name:
            raise ValueError(f"Can't send task, no queue name defined")

        producer: AIOKafkaProducer = await self.get_producer()

        try:
            res = await asyncio.wait_for(
                producer.send_and_wait(topic_name, payload, headers=headers), self.settings.request_timeout_ms*2
            )
        except asyncio.TimeoutError:
            self.logger.error(f"can't send task, sender timeout")
            # producer bug workaround, sender coroutine timeout means that producer enter to unrecoverable
            # state and waits for connection to broker to resume which never happens
            # close producer and reopen it
            try:
                # detach corrupted producer and stop it
                producer = self._producer
                del self._producer

                await asyncio.shield(asyncio.wait_for(producer.stop(), 10))
                del producer
            except asyncio.TimeoutError:
                self.logger.warning(f"can't stop producer, timeout")

            # re-try
            await self._send(payload, task, timeout)

        except UnknownTopicOrPartitionError:
            if self.missing_topic_handler(topic_name):
                await self._send(payload, task, timeout)
        except KafkaTimeoutError as exc:
            raise TimeoutError("Can't send task") from exc
        else:
            self.logger.debug(f"Kafka message delivered {res}")

    def mtb_error(self, topic_name: str):
        raise ValueError(f'no such topic: {topic_name}')

    def mtb_skip(self, topic_name: str):
        self.logger.info(f"message skipped due to missing topic {topic_name}")
        return False

    def mtb_create(self, topic_name: str):
        try:
            created = create_topics(topic_name,
                                    kafka_hosts=self.settings.kafka_hosts,
                                    request_timeout_ms=self.settings.request_timeout_ms,
                                    partitions_count=self.settings.default_partitions_count,
                                    replication_factor=self.settings.default_replication_factor,
                                    compression_type=self.settings.compression_type)
        except Exception as exc:
            self.logger.exception(
                f"unable to automatically create topic `{topic_name}`: {exc.__class__.__name__}({exc})"
            )
            return False

        if created:
            self.logger.debug(f"missing topic created: {topic_name}")

        return True

    async def get_producer(self):
        async with self._producer_lock:
            if hasattr(self, '_producer'):
                return self._producer
            else:
                await self._start_producer()
                return self._producer

    async def _start_producer(self):

        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.settings.kafka_hosts,
            acks=self.settings.ack_policy,
            request_timeout_ms=self.settings.request_timeout_ms,
            client_id=get_node_id()
        )

        self.logger.debug("producer created")

        try:
            await self._producer.start()
        except Exception as exc:
            self.logger.exception(f"unable to start Kafka producer: {exc.__class__.__name__}({exc})", exc_info=True)
            raise

        self.logger.debug("producer started")
