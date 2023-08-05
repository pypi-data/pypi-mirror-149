#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='py-esw',
    version='0.1.6',
    packages=find_packages(include=['esw', 'esw.*']),
    install_requires=[
        'requests>=2.26.0'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
