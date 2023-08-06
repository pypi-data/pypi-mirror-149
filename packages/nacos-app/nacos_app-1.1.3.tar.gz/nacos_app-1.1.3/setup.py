#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

current_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_dir, "README.md"), encoding='utf-8') as f:
    README = f.read()

packages = [
    'nacos_app'
]

setup(
    name='nacos_app',
    version='1.1.3',
    description='django-nacos-app',
    long_description=README,
    long_description_content_type="text/markdown",
    author_email="1593134926@qq.com",
    author="徐益庆",
    packages=packages,
    package_dir={'nacos_app': 'nacos_app'},
    include_package_data=True,
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    zip_safe=False,
)
