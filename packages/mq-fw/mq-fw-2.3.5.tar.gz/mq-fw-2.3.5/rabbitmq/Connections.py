# -*- coding: UTF-8 -*-
# @Time : 2021/12/2 下午5:55
# @Author : 刘洪波
from rabbitmq.Consumers import Consumer
from rabbitmq.Producers import Producer
from rabbitmq.Services import ConsumeProduce, ProduceConsume


class Connection(object):
    def __init__(self, host, port, username, password, heartbeat):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.heartbeat = heartbeat

    def create_consumer(self, exchange, routing_key, durable=False):
        """
        消费者
        :param exchange:
        :param routing_key:
        :param durable:
        :return:
        """
        return Consumer(self.host, self.port, self.username, self.password,
                        self.heartbeat, exchange, routing_key, durable)

    def create_producer(self, exchange, routing_key, durable=False):
        """
        生产者
        :param exchange:
        :param routing_key:
        :param durable:
        :return:
        """
        return Producer(self.host, self.port, self.username, self.password,
                        self.heartbeat, exchange, routing_key, durable)

    def consume_produce(self, consumer_exchange, consumer_routing_key,
                        producer_exchange, producer_routing_key, durable=False,
                        consumer_durable=None, producer_durable=None):
        """
        服务端（先消费再生产）
        :param consumer_exchange:
        :param consumer_routing_key:
        :param producer_exchange:
        :param producer_routing_key:
        :param durable:
        :param consumer_durable:
        :param producer_durable:
        :return:
        """
        return ConsumeProduce(self.create_consumer(consumer_exchange, consumer_routing_key,
                                                   consumer_durable if consumer_durable else durable),
                              self.create_producer(producer_exchange, producer_routing_key,
                                                   producer_durable if producer_durable else durable))

    def produce_consume(self, consumer_exchange, consumer_routing_key,
                        producer_exchange, producer_routing_key, durable=False,
                        consumer_durable=None, producer_durable=None):
        """
        调用端（先生产再消费）
        :param consumer_exchange:
        :param consumer_routing_key:
        :param producer_exchange:
        :param producer_routing_key:
        :param durable:
        :param consumer_durable:
        :param producer_durable:
        :return:
        """
        return ProduceConsume(self.create_consumer(consumer_exchange, consumer_routing_key,
                                                   consumer_durable if consumer_durable else durable),
                              self.create_producer(producer_exchange, producer_routing_key,
                                                   producer_durable if producer_durable else durable))
