# -*- coding: utf-8 -*-

import asyncio
import weakref
from functools import partial
from random import randint
from typing import List, Union, Tuple, Iterable, Set

from aiokafka import AIOKafkaConsumer, ConsumerRebalanceListener, ConsumerRecord
from humanize import naturalsize
from kafka import TopicPartition
from patchwork.core import AsyncSubscriber, Task
from patchwork.core.utils import AsyncQueue
from pydantic import root_validator

from .common import SECOND, get_node_id, MINUTE

# how much multiply some periods to get timeout value
MAX_TIME_MULTIPLIER = 10


class RebalanceListener(ConsumerRebalanceListener):
    """
    Lister for group assignment events, just to log current assignments
    """

    def __init__(self, worker):
        self.worker_ref = weakref.ref(worker)

    async def on_partitions_revoked(self, revoked):
        worker = self.worker_ref()
        if worker is None:
            return

        await worker.handle_partitions_revoke(revoked)

    async def on_partitions_assigned(self, assigned):
        worker = self.worker_ref()
        if worker is None:
            return

        await worker.handle_partitions_assignment(assigned)


class AsyncKafkaSubscriber(AsyncSubscriber):

    class Config(AsyncSubscriber.Config):
        """
        Kafka asynchronous client settings

        :cvar kafka_hosts:
            A comma separated hostnames with optional port number of bootstrap kafka brokers.
            Example: ```hostname1.mydomain,hostname2.mydomain:4000```
        :cvar topics:
            Initial list of topics to subscribe
        :cvar consumer_group: Name of consumer group
        :cvar metadata_validity_ms:
            Tells how long fetched metadata are valid, after this period Kafka Consumer will refresh metadatas
            Low value cause frequent metadata updates which may affect performance, however long period cause that
            new topics will be discovered later.
        :cvar health_check_ms:
            Determines how often Kafka broker should make a health-check calls to make sure that consumer is alive
            (in miliseconds)
        :cvar poll_interval_ms:
            Determine how ofter consumer should make a poll requests to Kafka broker (in miliseconds)
        """
        kafka_hosts: List[str]
        topics: List[str]
        consumer_group: str
        request_timeout_ms: int = 30*SECOND
        metadata_validity_ms: int = 5*MINUTE
        health_check_ms: int = 3*SECOND
        poll_interval_ms: int = 10*SECOND
        freeze_time: int = -1

        @root_validator
        def validate_freeze(cls, values):
            if values['freeze_time'] == -1:
                values['freeze_time'] = randint(
                    int(min(values['poll_interval_ms'] * MAX_TIME_MULTIPLIER / 0.5, 10 * SECOND)),
                    int(min(values['poll_interval_ms'] * MAX_TIME_MULTIPLIER * 0.75, 20 * SECOND))
                )/SECOND
            return values

    consumer: AIOKafkaConsumer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # internal job which fetches messages from Kafka using the consumer
        self._fetcher = None
        # task which freezes fetcher for some time after rebalance, on Kafka consumer can't commit on unassigned topic
        # so there is a chance that after rebalance currently processing task won't be commit-able and must be cancelled
        # to avoid to many cancels, wait after rebalance some time. It's common that multiple rebalances happens
        # in series on Kafka (eg. additional consumer reconnects or restarts)
        self._freezer = None

        self._getters_queue = AsyncQueue(maxsize=1)
        self._task_meta = {}
        self._subscribed = asyncio.Event()

    def __repr__(self):
        res = super().__repr__()
        return f"<{res[1:-1]} [brokers={','.join(self.settings.kafka_hosts)}]>"

    @property
    def max_poll_interval_ms(self):
        # max poll interval is 10 times greater than usual poll interval
        # if consumer does not make a poll request during this perion, Kafka broker will consider it as dead
        return self.settings.poll_interval_ms*MAX_TIME_MULTIPLIER

    @property
    def session_timeout(self):
        return self.settings.health_check_ms*MAX_TIME_MULTIPLIER

    def _on_task_ref_removed(self, ref, uuid):
        self._task_meta.pop(uuid)

    async def _start(self):
        """
        Starts the consumer and subscribes for given topics
        :return:
        """
        await self._start_consumer()

        if self.settings.topics:
            await self.subscribe(self.settings.topics)

        # https://github.com/aio-libs/aiokafka/issues/647
        # TODO: investigate this issue
        await asyncio.sleep(0.1)

    async def _stop(self):
        """
        Stops the consumer
        :return:
        """
        wait_for = []

        if self._freezer is not None:
            self._freezer.cancel()
            wait_for.append(self._freezer)

        if self._fetcher is not None:
            self._fetcher.cancel()
            wait_for.append(self._fetcher)

        if wait_for:
            await asyncio.wait(wait_for, timeout=1)

        try:
            await self.consumer.stop()
        except Exception as e:
            self.logger.exception(f"stopping kafka consumer failed {e.__class__.__name__}({e})")
        self.logger.debug("kafka consumer stopped")

    async def _fetch_one(self, timeout: float = None) -> Tuple[bytes, ConsumerRecord]:
        # TODO: add timeout support
        fut = self.loop.create_future()
        await self._getters_queue.put(fut)
        try:
            msg: ConsumerRecord = await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError as e:
            self._getters_queue.revoke_nowait(fut)
            raise TimeoutError() from e

        return msg.value, msg

    def _process_received_task(self, payload: bytes, meta: ConsumerRecord) -> Task:
        task = super()._process_received_task(payload, {
            **dict(meta.headers),
            'queue_name': meta.topic,
        })
        # keep some metadata about task for commit
        self._task_meta[task.uuid] = (
            meta.topic,
            meta.partition,
            meta.offset,
            weakref.ref(task, partial(self._on_task_ref_removed, uuid=task.uuid))
        )
        return task

    def _get_message_meta(self, task: Task):
        meta = self._task_meta.pop(task.uuid, None)
        if not meta:
            self.logger.error(f"no metadata for given task '{task.task_type} (uuid={task.uuid})'")
            raise KeyError()

        tp = TopicPartition(meta[0], meta[1])
        offset = meta[2]
        return tp, offset

    async def commit(self, task: Task, timeout: float = None):
        """
        Commits given task on Kafka by committing topic-partition task came from at
        task message offset.
        :param task:
        :param timeout:
        :return:
        """
        tp, offset = self._get_message_meta(task)

        try:
            # commit message
            await self.consumer.commit({
                tp: offset + 1
            })
            return True
        except Exception as exc:
            self.logger.exception(f"commit failed {exc.__class__.__name__}({exc})")
            # seek to fetch same task again
            self.consumer.seek(tp, offset)
            return False
        finally:
            # resume partition
            self.consumer.resume(tp)
            self.logger.debug(f"{tp} resumed")

    async def rollback(self, task: Task, timeout: float = None):
        tp, offset = self._get_message_meta(task)
        # seek just before rollback message
        self.consumer.seek(tp, offset)
        # and resume partition
        self.consumer.resume(tp)
        self.logger.debug(f"{tp} resumed")

    async def handle_partitions_revoke(self, revoked):
        """
        Called after consumer stop fetching messages from Kafka but BEFORE rebalance starts.
        :param revoked:
        :return:
        """
        self._subscribed.clear()

        self.logger.debug(f"Partitions revoked: {','.join(f'{r.topic}:{r.partition}' for r in revoked)}")
        if self._fetcher is not None:
            self._fetcher.cancel()

        if self._freezer is not None:
            # if there is any freezer, cancel it
            self._freezer.cancel()

    async def handle_partitions_assignment(self, new_assignment):
        """
        Called after rebalance finished but BEFORE fetching starts
        :param new_assignment:
        :return:
        """
        self._subscribed.set()
        self.logger.debug(f"Partitions assigned: {','.join(f'{a.topic}:{a.partition}' for a in new_assignment)}")

        if self.settings.freeze_time == 0:
            self._start_fetching()
            return

        async def unfreeze():
            # wait before consuming to give a time for consumer group to stabilize
            # randomize wait time to avoid fetch-storm on kafka when multiple consumers were created
            # at the same time
            # set wait time to at least 10 seconds (or half of max_poll_interval) and not greater than 20 seconds
            # or 3/4 of max_poll_interval. Freeze can't exceed max_poll_interval because in such case freeze
            # will cause considering client as dead by the Kafka broker due to no poll requests during max_poll_interval

            self.logger.info(f"Consumer freezed after partitions assignment for {self.settings.freeze_time} seconds")
            await asyncio.sleep(self.settings.freeze_time)

        # freeze must be as async task to avoid blocking rebalance as aiokafka waits for all handlers to
        # complete before committing rebalanced state to Kafka
        self._freezer = self.loop.create_task(unfreeze())
        self._freezer.add_done_callback(self._consumer_unfreezed)

    def _consumer_unfreezed(self, fut: asyncio.Future):
        self._freezer = None
        if fut.cancelled():
            self.logger.debug("consumer freeze cancelled")
            return

        exc = fut.exception()
        if exc is None:
            self.logger.info("consumer unfreezed")
            self._start_fetching()
        else:
            self.logger.exception(f"consumer unfreezing failed due an error {exc.__class__.__name__}({exc})")

    def _start_fetching(self):
        self._fetcher = self.loop.create_task(self._fetch_messages_task())
        self._fetcher.add_done_callback(self._fetch_messages_done)

    async def _fetch_messages_task(self):
        """
        This task fetches messages from kafka in given pool_interval_ms interval, even if processing
        queue is full. In such case received message is discarded and offsets not committed, so same
        message should be delivered again.
        Without periodic pooling consumer will be marked as dead by coordinator.
        :return:
        """
        while not self.is_stopping:

            msg: ConsumerRecord = await self.consumer.getone()

            try:
                # wait for getter not longer then half pool interval
                getter: asyncio.Future = await self._getters_queue.get(
                    timeout=self.settings.poll_interval_ms / 2 / SECOND
                )
            except asyncio.TimeoutError:
                # seek back to get same message again
                self.consumer.seek(TopicPartition(topic=msg.topic, partition=msg.partition), msg.offset)
                continue
            else:
                self._getters_queue.task_done()
                if getter.cancelled():
                    # seek back to get same message again
                    self.consumer.seek(TopicPartition(topic=msg.topic, partition=msg.partition), msg.offset)
                    continue

                getter.set_result(msg)

            msg_key = f'{msg.topic}:{msg.partition}@{msg.offset}'
            self.logger.debug(f"Message '{msg_key}' received ({naturalsize(len(msg.value))})")

            # pause the topic-partition to make sure that no more messages will be fetched
            # from this topic-partition
            tp = TopicPartition(topic=msg.topic, partition=msg.partition)
            self.consumer.pause(tp)
            self.logger.debug(f"{tp} paused")

    def _fetch_messages_done(self, fut):
        self._fetcher = None
        if fut.cancelled():
            return

        exc = fut.exception()
        if exc is not None:
            self.logger.error(f"fetching task terminated with exception {exc.__class__.__name__}({exc})", exc_info=exc)
            self._start_fetching()
        else:
            if self.is_stopping:
                self.logger.info("fetching task completed")
                return
            self.logger.error(f"fetching task unexpectedly done")
            self._start_fetching()

    async def _start_consumer(self):
        self.consumer = AIOKafkaConsumer(
            client_id=get_node_id(),
            bootstrap_servers=self.settings.kafka_hosts,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id=self.settings.consumer_group,
            metadata_max_age_ms=self.settings.metadata_validity_ms,
            # set max poll interval 10 times greater than poll internal
            max_poll_interval_ms=self.max_poll_interval_ms,
            # set session timeout 10 times greater than health-check
            session_timeout_ms=self.session_timeout,
            heartbeat_interval_ms=self.settings.health_check_ms,
            consumer_timeout_ms=self.settings.request_timeout_ms
        )
        self.logger.debug("consumer created")
        try:
            await self.consumer.start()
        except Exception as exc:
            self.logger.exception(f"unable to start Kafka consumer: {exc.__class__.__name__}({exc})", exc_info=True)
            raise
        self.logger.debug("consumer started")

    async def subscribe(self, queue_name: Iterable[str]):
        """
        Subscribes to the given queues (topics). This method makes incremental subscription.

        Note: if you need pattern subscription overload this method and decide how to play
        with mixed list - pattern subscriptions.
        :param queue_name:
        :return:
        """
        topics = self.consumer.subscription() | set(queue_name)
        self.consumer.subscribe(topics=list(topics), listener=RebalanceListener(self))

    async def unsubscribe(self, queue_name: Iterable[str]):
        """
        Unsubscribes from given queues (topics).
        :param queue_name:
        :return:
        """
        topics = self.consumer.subscription() ^ set(queue_name)
        self.consumer.subscribe(topics=list(topics), listener=RebalanceListener(self))

    async def subscription(self) -> Iterable[str]:
        return self.consumer.subscription()


class AssignKafkaSubscriber(AsyncKafkaSubscriber):
    """
    An alternative Kafka subscriber which uses `assign` method instead of `subscribe`.
    This subscribed may work with consumer group which enables offset commits or without it.

    If no CG is given subscriber is seeking to the end of assigned topics just after assignment.
    If CG is set, subscribed does not seek.

    This subscriber assigns only to partition 0 so it works only with topics which have one
    partition. If you'd like to work with multiple partitions overload subscribe/unsubscribe methods
    accordingly and decide on which condition assign partition to subscriber instances
    """

    class Config(AsyncKafkaSubscriber.Config):
        consumer_group: str = None
        topics: Union[List[str], str] = []

    async def subscribe(self, queue_name: Iterable[str]):
        assignment = self.consumer.assignment()
        queues: Set[TopicPartition] = set(TopicPartition(topic=t, partition=0) for t in queue_name)

        new_topics = queues - assignment
        if not new_topics:
            # nothing new to subscribe on
            return

        topics = assignment | queues

        self.consumer.assign(list(topics))
        if not self.settings.consumer_group:
            # seek to the end of each new topic subscribed so no historical messages will be fetched
            await self.consumer.seek_to_end(*new_topics)

        # manually call revoke/assign callbacks
        await self.handle_partitions_revoke(assignment)
        await self.handle_partitions_assignment(topics)

    async def unsubscribe(self, queue_name: Iterable[str]):
        queues: Set[TopicPartition] = set(TopicPartition(topic=t, partition=0) for t in queue_name)
        assignment = self.consumer.assignment()
        topics = assignment ^ queues

        self.consumer.assign(list(topics))

        # manually call revoke/assign callbacks
        await self.handle_partitions_revoke(assignment)
        await self.handle_partitions_assignment(topics)

    async def commit(self, task: Task, timeout: float = None):
        if self.settings.consumer_group:
            await super().commit(task, timeout)
        else:
            # no commits if no consumer group, just resume paused TP
            tp, _ = self._get_message_meta(task)

            self.consumer.resume(tp)
            self.logger.debug(f"{tp} resumed")
