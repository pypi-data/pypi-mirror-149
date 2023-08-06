# -*- coding: UTF-8 -*-
# @Time : 2022/4/12 上午11:16 
# @Author : 刘洪波
import pulsar

"""
consumer_type_dict 消费类型
参考网址：https://pulsar.apache.org/docs/en/concepts-messaging/
"""
consumer_type_dict = {
    'Shared': pulsar.ConsumerType.Shared,  # 共享模式
    'Exclusive': pulsar.ConsumerType.Exclusive,  # 独占模式
    'Failover': pulsar.ConsumerType.Failover,  # 灾备模式
    'KeyShared': pulsar.ConsumerType.KeyShared  # 关键字共享模式
}


def get_consumer_type(consumer_type):
    consumer_type = consumer_type_dict.get(consumer_type)
    return consumer_type if consumer_type else pulsar.ConsumerType.Shared
