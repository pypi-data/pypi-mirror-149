# -*- coding: UTF-8 -*-
# @Time : 2022/5/6 下午4:51 
# @Author : 刘洪波
from retry import retry
import pika
from pika import exceptions
import loguru
from rabbitmq.Consumers import Consumer
from rabbitmq.Producers import Producer


class ConsumeProduce(object):
    def __init__(self, consumer: Consumer, producer: Producer):
        self.consumer = consumer
        self.producer = producer

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
                self.producer.send(result)

        self.consumer.receive(callback, thread_count)


class ProduceConsume(object):
    def __init__(self, consumer: Consumer, producer: Producer):
        self.consumer = consumer
        self.producer = producer
        self.result = []

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
        if message_list:
            if not isinstance(message_list, list):
                raise ValueError('error type of parameter: message_list must be of type list')
            consume_num = len(message_list)

            @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3), logger=loguru.logger)
            def receive():
                if thread_count is not None:
                    if not isinstance(thread_count, int):
                        raise ValueError('error type of parameter: message_list must be of type int')
                channel, queue_name = self.consumer.create_channel(consume_num=consume_num)
                self.producer.send(message_list)

                def callback(body):
                    self.result.append(body)
                self.consumer.start_consume(callback, consume_num, channel, queue_name, thread_count)
            receive()
        return self.result
