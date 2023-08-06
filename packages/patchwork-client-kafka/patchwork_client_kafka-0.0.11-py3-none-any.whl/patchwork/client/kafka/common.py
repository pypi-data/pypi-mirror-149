# -*- coding: utf-8 -*-

from typing import List

import socket

import threading

import multiprocessing
from enum import Enum, IntEnum

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

MILISECOND = 1
SECOND = 1000*MILISECOND
MINUTE = 60*SECOND


class MissingTopicBehaviour(str, Enum):
    """
    Behaviour of missing topic
    """

    ERROR = 'error'
    """Raises an exception when topic is missing"""

    CREATE = 'create'
    """Automatically creates missing topic"""

    SKIP = 'skip'
    """
    Skips failure silently. Action won't be performed
    
    !!! danger
        Using this option is not recommended as may lead to data loss for instance when task
        destination topic doesn't exist    
    """


class CompressionType(str, Enum):
    """
    Compression type for producing messages. See compression options in
    [`aiokafka` documentation](https://aiokafka.readthedocs.io/en/stable/) to get know
    what requirements certain compressions have to work.
    """

    NONE = ''
    """No compression"""

    GZIP = 'gzip'
    """GZIP compression"""

    SNAPPY = 'snappy'
    """Snappy compression"""

    LZ4 = 'lz4'
    """LZ4 compression"""


class AckPolicy(IntEnum):
    """ACK policy for Kafka producer. See Kafka documentation for more details about acknowledgements"""

    NO_ACK = 0
    """No ACK, producer returns immediately after sending message without waiting for any acknowledgement"""

    ACK_LEADER = 1
    """Producer waits for ACK from the partition leader"""

    ACK_ALL = -1
    """Producer waits for ACK from all brokers which holds partition replications"""


def create_topics(
        *topic_names,
        kafka_hosts: str,
        request_timeout_ms: int,
        partitions_count: int,
        replication_factor: int,
        compression_type: str) -> List[NewTopic]:
    """
    A helper method to create missing topics. Already existing topics are not affected.

    :param topic_names:     an iterable of topic names to create
    :param kafka_hosts:     comma-separated list of kafka hosts
    :param request_timeout_ms:  requests timeout in miliseconds
    :param partitions_count:    number of partitions for newly created topics
    :param replication_factor:  replication factor for newly created topics
    :param compression_type:    default compression type for newly created topics
    :return: list of created topics
    """
    admin = KafkaAdminClient(bootstrap_servers=kafka_hosts, request_timeout_ms=request_timeout_ms)

    available_topics = set(admin.list_topics().keys())

    new_topics = []

    for tn in topic_names:
        if tn not in available_topics:
            new_topics.append(NewTopic(name=tn, num_partitions=partitions_count,
                                       replication_factor=replication_factor,
                                       topic_configs={'compression.type': compression_type}))

    if not new_topics:
        return []

    try:
        admin.create_topics(new_topics)
    except ValueError:
        # kafka-python 1.4.4 has a in kafka response processing (https://github.com/dpkp/kafka-python/issues/1657)
        pass
    except TopicAlreadyExistsError:
        # race-condition on create
        pass

    return new_topics


def get_node_id() -> str:
    """
    Helper which produce `client_id` for Kafka consumer and producer
    :return: client id
    """
    process_name = multiprocessing.current_process().name
    thread_name = threading.current_thread().name
    return f'{thread_name}.{process_name}@{socket.gethostname()}'
