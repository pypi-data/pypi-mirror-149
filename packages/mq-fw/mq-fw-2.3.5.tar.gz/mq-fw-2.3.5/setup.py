# -*- coding: UTF-8 -*-
# @Time : 2021/12/6 上午11:33 
# @Author : 刘洪波
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mq-fw',
    version='2.3.5',
    packages=setuptools.find_packages(),
    url='https://gitee.com/maxbanana',
    license='Apache',
    author='hongbo liu',
    author_email='782027465@qq.com',
    description='A message queue framework, including pulsar and rabbitmq',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pulsar-client>=2.8.0', 'pika>=1.1.0', 'retry>=0.9.2', 'loguru>=0.6.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)