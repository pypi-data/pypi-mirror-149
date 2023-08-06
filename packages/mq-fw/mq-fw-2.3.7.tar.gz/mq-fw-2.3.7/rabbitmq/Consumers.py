# -*- coding: UTF-8 -*-
# @Time : 2022/5/6 下午4:49 
# @Author : 刘洪波
from retry import retry
import pika
from pika import exceptions
from concurrent.futures import ThreadPoolExecutor
import loguru
"""
消费者
"""


class Consumer(object):
    def __init__(self, host, port, username, password, heartbeat, exchange, routing_key, durable=False, random_tag=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.heartbeat = heartbeat
        self.exchange = exchange
        self.routing_key = routing_key
        self.durable = durable
        self.consumed_num = 0  # 已经消费的次数
        self.random_tag = random_tag  # 是否随机 exchange， routing_key

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3), logger=loguru.logger)
    def receive(self, task, thread_count=None, consume_num=0):
        """
        消费者消费
        :param task:
        :param thread_count: 当thread_count 有值的时候，可以进行多线程并行消费
        :param consume_num: 消费consume_num 次就停止消费
        :return:
        """
        if thread_count is not None:
            if not isinstance(thread_count, int):
                raise ValueError('error type of parameter: message_list must be of type int')
        if not isinstance(consume_num, int):
            raise ValueError('error type of parameter: message_list must be of type int')
        channel, queue_name = self.create_channel()
        self.start_consume(task, consume_num, channel, queue_name, thread_count)

    def create_channel(self):
        loguru.logger.info('开始连接rabbitmq')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=pika.PlainCredentials(self.username, self.password),
            heartbeat=self.heartbeat)
        )
        loguru.logger.info('已连接至rabbitmq')
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type='topic', durable=self.durable)
        queue_name = self.routing_key + '.queue'
        try:
            channel.queue_declare(queue=queue_name, passive=True)
        except Exception as e:
            channel = connection.channel()
            channel.exchange_declare(exchange=self.exchange, exchange_type='topic', durable=self.durable)
            channel.queue_declare(queue=queue_name)
            channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.routing_key)
        return channel, queue_name

    def start_consume(self, task, consume_num, channel, queue_name, thread_count):
        if thread_count:
            pool = ThreadPoolExecutor(max_workers=thread_count)

        self.consumed_num = 0  # 已经消费的次数

        def callback(ch, method, properties, body):
            body = body.decode('utf8')
            if thread_count:
                pool.submit(task, body)
            else:
                task(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if consume_num:
                self.consumed_num += 1
                if self.consumed_num == consume_num:
                    ch.stop_consuming()
                    if self.random_tag:
                        ch.queue_delete(queue_name)
                        ch.exchange_delete(self.exchange)

        channel.basic_consume(queue=queue_name, auto_ack=False, on_message_callback=callback)
        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
