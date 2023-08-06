# -*- coding: UTF-8 -*-
# @Time : 2021/12/3 下午6:36 
# @Author : 刘洪波


def connect(host, port, username, password, url):
    from RabbitmqPulsar.Connections import Interconnection
    return Interconnection(host, port, username, password, url)
