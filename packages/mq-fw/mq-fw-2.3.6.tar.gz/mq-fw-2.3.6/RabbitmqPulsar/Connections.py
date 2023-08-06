# -*- coding: UTF-8 -*-
# @Time : 2022/4/15 下午9:51 
# @Author : 刘洪波
import pulsar_mq
import rabbitmq
from RabbitmqPulsar.Services import RabbitmqToPulsar, PulsarToRabbitmq, InterService, InterServiceRB, InterServicePS


"""
rabbitmq 和 pulsar互相订阅消费
"""


class Interconnection(object):
    def __init__(self, rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, pulsar_url, heartbeat):
        """
        rabbitmq 和 pulsar 连接
        """
        self.rabbitmq_connect = rabbitmq.connect(rabbitmq_host, rabbitmq_port,
                                                 rabbitmq_username, rabbitmq_password, heartbeat)
        self.pulsar_client = pulsar_mq.client(pulsar_url)

    def rabbitmq_to_pulsar(self):
        """
        1. 订阅rabbitmq
        2. 处理消费的数据
        3. 将处理后的数据 发送到 pulsar
        """
        return RabbitmqToPulsar(self.rabbitmq_connect, self.pulsar_client)

    def pulsar_to_rabbitmq(self):
        """
        1. 订阅 pulsar
        2. 处理消费的数据
        3. 将处理后的数据发送到 rabbitmq
        """
        return PulsarToRabbitmq(self.rabbitmq_connect, self.pulsar_client)

    def inter_services(self, start_with_rabbitmq=True, random_queue=True):
        """
        rabbitmq 与 pulsar 互联服务

        :param start_with_rabbitmq:
                1. 值为True时， 从 rabbitmq 订阅，将数据发送至 pulsar;
                   并且从 pulsar 订阅，将数据发送至 rabbitmq

                2. 值为False时，从 pulsar 订阅，将数据发送至 rabbitmq；
                   并且从 rabbitmq 订阅，将数据发送至 pulsar;
        :param random_queue:  当start_with_rabbitmq=True时，pulsar是否使用随机队列来生产消息，
                              当start_with_rabbitmq=False时, rabbitmq是否使用随机队列来生产消息

                1. 值为True时，使用随机队列来生产消息
                2. 值为False时，不使用随机队列来生产消息

                建议使用随机队列
        :return:
        """
        if start_with_rabbitmq:
            if random_queue:
                return InterServiceRB(self.rabbitmq_connect, self.pulsar_client)
        else:
            if random_queue:
                return InterServicePS(self.rabbitmq_connect, self.pulsar_client)
        return InterService(self.rabbitmq_connect, self.pulsar_client)
