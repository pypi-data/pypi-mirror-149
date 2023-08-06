# -*- coding: UTF-8 -*-
# @Time : 2022/5/6 下午4:51 
# @Author : 刘洪波
from retry import retry
import pika
from pika import exceptions
import loguru
import json
import random
from rabbitmq.Consumers import Consumer
from rabbitmq.Producers import Producer


class ConsumeProduce(object):
    def __init__(self, consumer: Consumer, producer: Producer, create_producer):
        self.consumer = consumer
        self.producer = producer
        self.create_producer = create_producer

    def run(self, task,  thread_count=None):
        """
        rabbitmq 服务端
        1. 订阅rabbitmq
        2. 处理消费的数据
        3. 发送得到的结果
        :param task:
        :param thread_count:
        :return:
        """

        def callback(body):
            result = task(body)
            if result:
                rr = json.loads(body)
                random_exchange = rr.get('random_exchange')
                random_routing_key = rr.get('random_routing_key')
                if self.create_producer:
                    if random_exchange and random_routing_key:
                        self.producer = self.create_producer(random_exchange, random_routing_key)
                    else:
                        raise ValueError('producer_exchange and producer_routing_key is None, '
                                         'need producer_exchange and producer_routing_key')
                self.producer.send(result)

        self.consumer.receive(callback, thread_count)


class ProduceConsume(object):
    def __init__(self, consumer: Consumer, producer: Producer, create_consume):
        self.consumer = consumer
        self.producer = producer
        self.create_consumer = create_consume

    def run(self, message_list: list, thread_count=None):
        """
        rabbitmq 调用端
        1. 往发rabbitmq送消息
        2. 订阅rabbitmq
        3. 消费得到服务端返回的结果
        :param message_list:
        :param thread_count:
        :return:
        """

        def produce_num(num_len: int):
            random_num = ''
            for i in range(num_len):
                random_num += str(random.randint(0, 9))
            return random_num

        def produce_num2(num_len: int, x):
            random_num = ''
            random_num += str(produce_num(x))
            for i in range(1, num_len):
                random_num += '.' + str(produce_num(x))
            return random_num

        result = []
        if message_list:
            if not isinstance(message_list, list):
                raise ValueError('error type of parameter: message_list must be of type list')
            random_exchange = None
            random_routing_key = None
            if self.create_consumer:
                random_exchange = produce_num2(3, 4)
                random_routing_key = produce_num2(3, 4)
                self.consumer = self.create_consumer(random_exchange, random_routing_key, random_tag=True)
            consume_num = len(message_list)

            @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3), logger=loguru.logger)
            def receive():
                if thread_count is not None:
                    if not isinstance(thread_count, int):
                        raise ValueError('error type of parameter: message_list must be of type int')
                channel, queue_name = self.consumer.create_channel()
                self.producer.send(message_list, random_exchange, random_routing_key)

                def callback(body):
                    result.append(body)
                self.consumer.start_consume(callback, consume_num, channel, queue_name, thread_count)
            receive()
        return result
