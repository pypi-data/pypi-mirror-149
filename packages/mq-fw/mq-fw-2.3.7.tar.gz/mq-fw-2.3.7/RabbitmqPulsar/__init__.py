# -*- coding: UTF-8 -*-
# @Time : 2021/12/3 下午6:36 
# @Author : 刘洪波
from RabbitmqPulsar.Connections import Interconnection


def connect(host, port, username, password, url, heartbeat=60):
    return Interconnection(host, port, username, password, url, heartbeat)
