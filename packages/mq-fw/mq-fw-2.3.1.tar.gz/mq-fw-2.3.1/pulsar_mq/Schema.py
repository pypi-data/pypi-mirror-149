# -*- coding: UTF-8 -*-
# @Time : 2022/4/12 下午2:45 
# @Author : 刘洪波
"""
schema 消息类型
参考网址：https://pulsar.apache.org/docs/en/client-libraries-python/
Schema	Notes
BytesSchema	Get the raw payload as a bytes object. No serialization/deserialization are performed. This is the default schema mode
StringSchema	Encode/decode payload as a UTF-8 string. Uses str objects
JsonSchema	Require record definition. Serializes the record into standard JSON payload
AvroSchema	Require record definition. Serializes in AVRO format
"""
import pulsar


def StringSchema():
    return pulsar.schema.StringSchema()


def BytesSchema():
    return pulsar.schema.BytesSchema()


def JsonSchema(record_cls):
    return pulsar.schema.JsonSchema(record_cls)


def AvroSchema(record_cls):
    return pulsar.schema.AvroSchema(record_cls)
