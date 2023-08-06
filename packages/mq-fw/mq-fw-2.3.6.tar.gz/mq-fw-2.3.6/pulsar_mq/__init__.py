# -*- coding: UTF-8 -*-
# @Time : 2021/11/27 下午5:09 
# @Author : 刘洪波
from pulsar_mq.Clients import Client


def client(url: str):
    return Client(url)
