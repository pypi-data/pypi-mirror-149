# -*- coding: UTF-8 -*-
# @Time : 2021/12/1 下午4:04 
# @Author : 刘洪波
import json
import time
import pulsar
from pulsar_mq.ConsumerType import get_consumer_type
from pulsar_mq.Producers import Producer
from pulsar_mq.Consumers import Consumer
from pulsar_mq.Schema import StringSchema

"""
pulsar服务
一、 ConsumeProduce
1. 订阅pulsar
2. 处理消费的数据
3. 发送业务数据
4. 发送的 队列 可以是 随机的

二、 ProduceConsume

1. 发送数据至pulsar
2. 订阅pulsar得到业务数据
3. 消费的 队列 可以是 随机的
"""


class ConsumeProduce(object):
    """订阅得到业务数据，经处理过后发送"""

    def __init__(self, client: pulsar.Client, consumer_topic, consumer_name: str, consumer_type, producer_topic=None,
                 schema=StringSchema()):
        """
        创建 生产者 和 消费者
        :param client:
        :param consumer_topic:
        :param consumer_name:
        :param producer_topic:
        :param schema:
        """
        self.client = client
        self.sch = schema
        self.consumer = Consumer(client, consumer_topic, consumer_name, schema=schema, consumer_type=consumer_type)
        self.producer_topic = producer_topic

    def run(self, task, thread_count=None, _async=True, callback=None, logger=None):
        """
        :param task: 任务程序
        :param thread_count: 指定最大线程数
        :param _async: 是否异步发送消息， True异步发送， Flase 同步发送
        :param callback: 异步发送的回调函数
        :param logger: 日志收集器
        :return:
        """

        def send_task(msg):
            result = task(msg)
            data = json.loads(msg.data())
            random_topic = data.get('random_topic')
            if self.producer_topic:
                producer = Producer(self.client, self.producer_topic, schema=self.sch)
            elif random_topic:
                producer = Producer(self.client, random_topic, schema=self.sch)
            else:
                raise ValueError('producer_topic and random_topic is None, need producer topic')
            producer.send(result, _async=_async, callback=callback)
            producer.close()

        self.consumer.receive(send_task, thread_count, logger)


class ProduceConsume(object):
    """发送数据至pulsar，订阅pulsar得到业务数据"""

    def __init__(self, client: pulsar.Client, producer_topic, consumer_type, consumer_topic=None, consumer_name=None,
                 schema=StringSchema()):
        self.client = client
        self.sch = schema
        self.consumer_topic = consumer_topic
        self.consumer_name = consumer_name
        self.consumer_type = get_consumer_type(consumer_type)
        self.producer = Producer(client, producer_topic, schema=schema)

    def run(self, data, timeout_millis=300000, _async=True, callback=None):
        """
        :param data: 输入格式为json
        :param timeout_millis: 订阅超时
        :param _async: 是否异步发送消息， True异步发送， Flase 同步发送
        :param callback: 异步发送的回调函数
        :return:
        """
        def do(_consumer_topic, _consumer_name, _random_topic):
            consumer = self.client.subscribe(_consumer_topic, _consumer_name, schema=self.sch,
                                             consumer_type=self.consumer_type)
            self.producer.send(data, _async=_async, callback=callback, random_topic=_random_topic)
            msgs = []
            if isinstance(data, list):
                for i in range(len(data)):
                    msg = consumer.receive(timeout_millis)
                    consumer.acknowledge(msg)
                    msgs.append(msg)
                consumer.unsubscribe()
                return msgs
            elif isinstance(data, str):
                msg = consumer.receive(timeout_millis)
                consumer.acknowledge(msg)
                consumer.unsubscribe()
                return msg
            else:
                raise ValueError('the data type sent is wrong, the required type is list or str')

        if self.consumer_topic and self.consumer_name:
            return do(self.consumer_topic, self.consumer_name, False)
        else:
            if self.consumer_topic is None and self.consumer_name is None:
                random_topic = 'random_topic_' + str(int(round(time.time() * 1000000)))
                return do(random_topic, random_topic, random_topic)
            elif self.consumer_topic:
                raise ValueError('consumer_name is None, need consumer_name')
            elif self.consumer_name:
                raise ValueError('consumer_topic is None, need consumer_topic')
