#!/usr/bin/env python3

from setuptools import setup

setup(
    name='tscounters-py',
    version='0.0.3',
    description='Time-series counters',
    author='Jiaxin Cao',
    author_email='Jiaxin.Cao@gmail.com',
    packages=['tscounters'],
    url="https://github.com/jiaxincao/tscounters-py",
    keywords="opentsdb, metrics, counters",
    install_requires=[
        "requests",
        "prometheus_client",
    ]
)
