# -*- coding: UTF-8 -*-
# @Time : 2022/5/6 下午4:50 
# @Author : 刘洪波
import pika
"""
生产者
生产数据
"""


class Producer(object):
    def __init__(self, host, port, username, password, heartbeat, exchange, routing_key, durable=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.exchange = exchange
        self.heartbeat = heartbeat
        self.routing_key = routing_key
        self.durable = durable

    def send(self, message_list: list):
        """
        发送数据
        :param message_list: 可以一次发送多条消息
        :return:
        """
        if not isinstance(message_list, list):
            raise ValueError('error type of parameter: message_list must be of type list')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=pika.PlainCredentials(self.username, self.password),
            heartbeat=self.heartbeat)
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type='topic', durable=self.durable)
        for message in message_list:
            channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message)
        connection.close()
