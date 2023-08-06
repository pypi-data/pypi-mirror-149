# -*- coding: UTF-8 -*-
# @Time : 2022/5/6 下午4:51 
# @Author : 刘洪波
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
            self.producer.send(message_list)

            def callback(body):
                self.result.append(body)

            self.consumer.receive(callback, thread_count, len(message_list))
        return self.result
