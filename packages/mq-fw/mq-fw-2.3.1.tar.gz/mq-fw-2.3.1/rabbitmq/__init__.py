# -*- coding: UTF-8 -*-
# @Time : 2021/12/2 下午5:54 
# @Author : 刘洪波
from rabbitmq.Connections import Connection


def connect(host, port, username, password, heartbeat=60):
    # heartbeat 心跳检测，默认60秒检测一次心跳
    return Connection(host, port, username, password, heartbeat)
