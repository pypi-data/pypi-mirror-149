# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 9:39
# @Author  : xuyiqing
# @FileName: service.py
import logging

from nacos_app.obj import Instance
from nacos_app.register import NacosServerDiscoveryRegister


logger = logging.getLogger("nacos")
if not logger.handlers:
    logger = logging.getLogger("django")


class NacosServerInstance(NacosServerDiscoveryRegister):

    def __init__(self, **kwargs):
        super(NacosServerInstance, self).__init__(**kwargs)

    def get_instances(self, service_name: str):
        url = "http://{}/nacos/v1/ns/instance/list".format(self.get_server_addr())
        params = {
            "serviceName": service_name,
            "groupName": self.group_name,
            "namespaceId": self.namespace,
            "healthyOnly": True,
            "accessToken": self.access_token
        }
        resp = self.send_request("GET", url, params=params).json()
        hosts = resp["hosts"]
        instances = []
        for host in hosts:
            instance = Instance(**host)
            instances.append(instance)
        return instances
