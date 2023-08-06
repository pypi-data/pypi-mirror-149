# -*- coding: UTF-8 -*-
# @Time : 2021/12/3 下午7:05 
# @Author : 刘洪波
import time
from concurrent.futures import ThreadPoolExecutor
from pulsar_mq.Clients import Client
from rabbitmq.Connections import Connection


class RabbitmqToPulsar(object):
    def __init__(self, rabbitmq_connect: Connection, pulsar_client: Client):
        """
        rabbitmq 和 pulsar 连接
        """
        self.rabbitmq_connect = rabbitmq_connect
        self.pulsar_client = pulsar_client

    def run(self, task, pulsar_topic, rabbitmq_exchange, rabbitmq_routing_key, durable=False,
            rabbitmq_thread_count=None, _async=True, send_callback=None, random_topic=None, logger=None):
        """
        1. 订阅rabbitmq
        2. 处理消费的数据
        3. 将处理后的数据 发送到 pulsar
        :param task:  该函数是处理消费的数据
        :param pulsar_topic:
        :param random_topic: 随机 队列
        :param rabbitmq_exchange:
        :param rabbitmq_routing_key:
        :param durable:
        :param rabbitmq_thread_count:
        :param _async:  pulsar是否异步发送
        :param send_callback: pulsar异步发送时的回调函数
        :param logger: 日志收集器
        :return:
        """
        try:
            producer = self.pulsar_client.create_producer(pulsar_topic)
            consumer = self.rabbitmq_connect.create_consumer(rabbitmq_exchange, rabbitmq_routing_key, durable)

            def callback(msg):
                result = task(msg)
                if result:
                    producer.send(result, _async=_async, callback=send_callback, random_topic=random_topic)

            consumer.receive(callback, rabbitmq_thread_count)
        except Exception as e:
            if logger:
                logger.error(e)
            else:
                print(e)


class PulsarToRabbitmq(object):
    def __init__(self, rabbitmq_connect: Connection, pulsar_client: Client):
        """
        rabbitmq 和 pulsar 连接
        """
        self.rabbitmq_connect = rabbitmq_connect
        self.pulsar_client = pulsar_client

    def run(self, task, rabbitmq_exchange, rabbitmq_routing_key,
            pulsar_consumer_topic=None, pulsar_consumer_name=None,
            durable=False, pulsar_thread_count=None, logger=None):
        """
        1. 订阅 pulsar
        2. 处理消费的数据
        3. 将处理后的数据发送到 rabbitmq
        :param task:
        :param pulsar_consumer_topic:
        :param pulsar_consumer_name:
        :param rabbitmq_exchange:
        :param rabbitmq_routing_key:
        :param pulsar_thread_count:
        :param durable:
        :param logger:
        :return:
        """
        try:
            if pulsar_consumer_topic and pulsar_consumer_name:
                consumer = self.pulsar_client.create_consumer(pulsar_consumer_topic, pulsar_consumer_name)
            else:
                raise ValueError('pulsar error: consumer_topic and random_topic is None, need consumer topic')

            producer = self.rabbitmq_connect.create_producer(rabbitmq_exchange, rabbitmq_routing_key, durable)

            def callback(msg):
                result = task(msg)
                if result:
                    producer.send(result)

            consumer.receive(callback, pulsar_thread_count, logger)
        except Exception as e:
            if logger:
                logger.error(e)
            else:
                print(e)


class InterService(object):
    def __init__(self, rabbitmq_connect, pulsar_client):
        """
        rabbitmq 和 pulsar 连接
        """
        self.rabbitmq_connect = rabbitmq_connect
        self.pulsar_client = pulsar_client
        self.rabbitmq_to_pulsar = RabbitmqToPulsar(rabbitmq_connect, pulsar_client)
        self.pulsar_to_rabbitmq = PulsarToRabbitmq(rabbitmq_connect, pulsar_client)

    def run(self, pulsar_producer_topic, rabbitmq_send_exchange, rabbitmq_send_routing_key,
            rabbitmq_consumer_exchange,
            rabbitmq_consumer_routing_key, pulsar_consumer_topic, pulsar_consumer_name, send_task=None,
            consumer_task=None, durable=False,
            consumer_durable=None, producer_durable=None,
            _async=True, send_callback=None, rabbitmq_thread_count=None, pulsar_thread_count=None,
            logger=None):
        """
        1. 从 rabbitmq 订阅，将数据发送至 pulsar;
        2. 从 pulsar 订阅，将数据发送至 rabbitmq
        :param send_task:
        :param consumer_task:
        :param pulsar_producer_topic:
        :param pulsar_consumer_topic:
        :param pulsar_consumer_name:
        :param rabbitmq_send_exchange:
        :param rabbitmq_send_routing_key:
        :param rabbitmq_consumer_exchange:
        :param rabbitmq_consumer_routing_key:
        :param durable:
        :param consumer_durable:
        :param producer_durable:
        :param _async:
        :param send_callback:
        :param rabbitmq_thread_count:
        :param pulsar_thread_count:
        :param logger:
        :return:
        """
        if logger:
            def send_task2(msg):
                logger.info('取rabbitmq的消息：')
                logger.info(msg)
                return msg

            def consumer_task2(msg):
                logger.info('取pulsar的消息：')
                logger.info(msg.data())
                return [msg.data()]
        else:
            def send_task2(msg):
                return msg

            def consumer_task2(msg):
                return [msg.data()]

        if send_task is None:
            send_task = send_task2
        if consumer_task is None:
            consumer_task = consumer_task2
        pool = ThreadPoolExecutor(max_workers=2)
        pool.submit(self.rabbitmq_to_pulsar.run, send_task, pulsar_producer_topic, rabbitmq_consumer_exchange,
                    rabbitmq_consumer_routing_key, durable=consumer_durable if consumer_durable else durable,
                    rabbitmq_thread_count=rabbitmq_thread_count,
                    _async=_async, send_callback=send_callback, logger=logger)
        pool.submit(self.pulsar_to_rabbitmq.run, consumer_task, rabbitmq_send_exchange, rabbitmq_send_routing_key,
                    pulsar_consumer_topic=pulsar_consumer_topic, pulsar_consumer_name=pulsar_consumer_name,
                    durable=producer_durable if producer_durable else durable,
                    pulsar_thread_count=pulsar_thread_count, logger=logger)


class InterServiceRQ(object):
    def __init__(self, rabbitmq_connect: Connection, pulsar_client: Client):
        """
        rabbitmq 和 pulsar 连接
        """
        self.rabbitmq_connect = rabbitmq_connect
        self.pulsar_client = pulsar_client

    def run(self, pulsar_producer_topic, rabbitmq_send_exchange, rabbitmq_send_routing_key,
            rabbitmq_consumer_exchange, rabbitmq_consumer_routing_key,
            send_task=None, consumer_task=None, durable=False,
            consumer_durable=None, producer_durable=None,
            _async=True, send_callback=None, thread_count=5, logger=None):
        """
        从 rabbitmq 订阅，将数据发送至 pulsar;
        再从 pulsar 订阅，将数据发送至 rabbitmq
        :param send_task:
        :param consumer_task:
        :param pulsar_producer_topic:
        :param rabbitmq_send_exchange:
        :param rabbitmq_send_routing_key:
        :param rabbitmq_consumer_exchange:
        :param rabbitmq_consumer_routing_key:
        :param durable:
        :param consumer_durable:
        :param producer_durable:
        :param _async:
        :param send_callback:
        :param thread_count:
        :param logger:
        :return:
        """
        if logger:
            def send_task2(msg):
                logger.info('rabbitmq的输入：')
                logger.info(msg)
                return msg

            def consumer_task2(msg):
                logger.info('pulsar的输出：')
                logger.info(msg.data())
                return [msg.data()]
        else:
            def send_task2(msg):
                return msg

            def consumer_task2(msg):
                return [msg.data()]

        if send_task is None:
            send_task = send_task2
        if consumer_task is None:
            consumer_task = consumer_task2

        rb_consumer = self.rabbitmq_connect.create_consumer(rabbitmq_consumer_exchange, rabbitmq_consumer_routing_key,
                                                            consumer_durable if consumer_durable else durable)
        rb_producer = self.rabbitmq_connect.create_producer(rabbitmq_send_exchange, rabbitmq_send_routing_key,
                                                            producer_durable if producer_durable else durable)

        producer = self.pulsar_client.create_producer(pulsar_producer_topic)
        pool = ThreadPoolExecutor(max_workers=thread_count)

        def callback(msg):
            result = send_task(msg)
            if result:
                random_topic = 'random_topic_' + str(int(round(time.time() * 1000000)))

                def send_consume():
                    consumer = self.pulsar_client.create_consumer(random_topic, random_topic)
                    producer.send(result, _async=_async, callback=send_callback, random_topic=random_topic)

                    def callback_task(_msg):
                        consumer_result = consumer_task(_msg)
                        if consumer_result:
                            rb_producer.send(consumer_result)

                    consumer.receive_one(callback_task, logger)

                pool.submit(send_consume)

        rb_consumer.receive(callback)
