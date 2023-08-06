# -*- coding: UTF-8 -*-
# @Time : 2022/4/15 下午9:51 
# @Author : 刘洪波
import pulsar_mq
import rabbitmq


"""
rabbitmq 和 pulsar互相订阅消费
"""


class Interconnection(object):
    def __init__(self, rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password, pulsar_url):
        """
        rabbitmq 和 pulsar 连接
        """
        self.rabbitmq_connect = rabbitmq.connect(rabbitmq_host, rabbitmq_port, rabbitmq_username, rabbitmq_password)
        self.pulsar_client = pulsar_mq.client(pulsar_url)

    def rabbitmq_to_pulsar(self):
        """
        1. 订阅rabbitmq
        2. 处理消费的数据
        3. 将处理后的数据 发送到 pulsar
        """
        from RabbitmqPulsar.Services import RabbitmqToPulsar
        return RabbitmqToPulsar(self.rabbitmq_connect, self.pulsar_client)

    def pulsar_to_rabbitmq(self):
        """
        1. 订阅 pulsar
        2. 处理消费的数据
        3. 将处理后的数据发送到 rabbitmq
        """
        from RabbitmqPulsar.Services import PulsarToRabbitmq
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
                              当start_with_rabbitmq=False时, 此参数不工作

                1. 值为True时，pulsar使用随机队列来生产消息
                2. 值为False时，pulsar不使用随机队列来生产消息

                建议使用随机队列
        :return:
        """
        if start_with_rabbitmq:
            if random_queue:
                from RabbitmqPulsar.Services import InterServiceRQ
                return InterServiceRQ(self.rabbitmq_connect, self.pulsar_client)
            from RabbitmqPulsar.Services import InterService
            return InterService(self.rabbitmq_connect, self.pulsar_client)
        else:
            from RabbitmqPulsar.Services import InterService
            return InterService(self.rabbitmq_connect, self.pulsar_client)
