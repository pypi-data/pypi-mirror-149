#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

current_dir = os.path.dirname(os.path.realpath(__file__))

packages = [
    'nacos_app'
]

long_description = """
1、适用于Django服务程序注册微服务实例至nacos服务中心;
2、实现了服务与注册中心的登录授权，服务注册，心跳检测，服务调用负载均衡;
3、cloud模块作为一个django app注册，在INSTALLED_APPS加入'nacos_app.apps.NacosRegisterConfig'
4、django程序需要在settings环境中配置服务注册的信息NACOS_SERVER_DISCOVERY
5、gunicorn多个worker模式下启动需要添加--preload参数，由管理进程预加载非函数式编程中的代码块，从而避免多个worker同时加载register
   gunicorn backend.wsgi -w 8 -b 0.0.0.0:port -t 600 --preload
NACOS_SERVER_DISCOVERY = {
    "server_addr": "",                    # nacos服务中心地址
    "namespace": "",                      # 命名空间
    "group_name": "",                     # 分组
    "ip": "",                             # 本机ip
    "port": "",                           # 本机服务端口
    "service_name": "",                   # 本机服务名称
    "ephemeral": True,                    # 是否临时实例，true为临时实例，临时实例用于服务临时扩展，过后丢弃
    "username": "",                       # 拥有对应命名空间权限的账户
    "password": "",                       # 密码
    "heartbeat_interval": 6               # 心跳检测间隔，单位秒
}
"""

setup(
    name='nacos_app',
    version='1.1.2',
    description='djagno-nacos-app',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="1593134926@qq.com",
    author="徐益庆",
    packages=packages,
    package_dir={'nacos_app': 'nacos_app'},
    include_package_data=True,
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    zip_safe=False,
)
