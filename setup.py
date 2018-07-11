#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

from setuptools import setup

setup(
    name='purrsync',
    version='0.1.1',
    packages=['purrsync'],
    entry_points={
        'console_scripts': [
            'purrsync = purrsync.__main__:main'
        ]
    })
