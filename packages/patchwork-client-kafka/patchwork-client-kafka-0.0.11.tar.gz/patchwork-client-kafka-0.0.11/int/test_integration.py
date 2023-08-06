# -*- coding: utf-8 -*-
import uuid
from google.protobuf.wrappers_pb2 import BytesValue
from kafka import TopicPartition

from patchwork.client.kafka.publisher import AsyncKafkaPublisher
from patchwork.client.kafka.subscriber import AsyncKafkaSubscriber
from patchwork.core import Task
from patchwork.core.testutils.cases import AsyncioTestCase


class AsyncPublisherTestCase(AsyncioTestCase):

    @AsyncioTestCase.runUntilComplete
    async def test_lifetime(self):
        publisher = AsyncKafkaPublisher(kafka_hosts=['127.0.0.1:9092'])
        await publisher.run()

        self.assertTrue(publisher.is_running)
        await publisher.terminate()

        self.assertFalse(publisher.is_running)


class AsyncSubscriberTestCase(AsyncioTestCase):

    @AsyncioTestCase.runUntilComplete
    async def test_lifetime(self):
        subscriber = AsyncKafkaSubscriber(kafka_hosts=['127.0.0.1:9092'], topics=['test-topic'], consumer_group='test')
        await subscriber.run()
        self.assertTrue(subscriber.is_running)
        await subscriber.terminate()

        self.assertFalse(subscriber.is_running)


class AsyncIntegrationTest(AsyncioTestCase):

    @AsyncioTestCase.runUntilComplete
    async def test_simple_delivery(self):
        publisher = AsyncKafkaPublisher(kafka_hosts=['127.0.0.1:9092'])
        subscriber = AsyncKafkaSubscriber(
            kafka_hosts=['127.0.0.1:9092'],
            topics=['test-topic'],
            freeze_time=0,
            consumer_group='test'
        )

        await subscriber.run()
        await subscriber.consumer.seek_to_end(TopicPartition(topic='test-topic', partition=0))
        await publisher.run()

        gid = str(uuid.uuid4())
        payload = BytesValue(value=b'payload')
        message = Task()
        message.uuid = gid
        message.meta.queue_name = 'test-topic'
        message.task_type = 'test'
        message.payload.Pack(payload)

        await publisher.send(message)
        try:
            received = await subscriber.get(timeout=50)
        except TimeoutError:
            received = None
        await publisher.terminate()
        await subscriber.terminate()

        self.assertIsNotNone(received, msg="no task received")
        self.assertEqual(gid, received.uuid)

        received_payload = BytesValue()
        received.payload.Unpack(received_payload)
        self.assertEqual(b'payload', received_payload.value)
