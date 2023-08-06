# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 10:26
# @Author  : xuyiqing
# @FileName: obj.py

class Instance(object):

    def __init__(self, **kwargs):
        self.data = kwargs
        self.ip = kwargs.get("ip")
        self.port = kwargs.get("port")
        self.service_name = kwargs.get("serviceName")
        self.instance_id = kwargs.get("instanceId")
        self.healthy = kwargs.get("healthy")
        self.host = "{}:{}".format(self.ip, self.port)

    def __repr__(self):
        return "Instance--{}".format(self.data)
