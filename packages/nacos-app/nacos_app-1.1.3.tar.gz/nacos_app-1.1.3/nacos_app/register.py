# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 9:46
# @Author  : xuyiqing
# @FileName: register.py
import datetime
import json
import logging
import random
import time

import requests

from nacos_app.util import get_innerip

logger = logging.getLogger("nacos")
if not logger.handlers:
    logger = logging.getLogger("django")


class NacosServerDiscoveryRegister(object):

    def __init__(self, **kwargs):
        assert kwargs.get("server_addr"), "nacos服务注册地址不可为空"
        assert kwargs.get("namespace"), "命名空间不可为空"
        assert kwargs.get("group_name"), "组名不可为空"
        assert kwargs.get("port"), "本机服务端口不可为空"
        assert kwargs.get("service_name"), "服务名称不可为空"
        assert kwargs.get("username"), "授权账号不可为空"
        assert kwargs.get("password"), "授权密码不可为空"

        self.server_addrs = kwargs["server_addr"].strip(",").split(",")
        assert self.server_addrs, "nacos服务注册地址不可为空"
        self.namespace = kwargs["namespace"]
        self.group_name = kwargs["group_name"]
        ip = get_innerip()
        if ip:
            self.ip = ip
        else:
            assert kwargs.get("ip"), "本机服务ip不可为空"
            self.ip = kwargs["ip"]
        self.port = kwargs["port"]
        self.service_name = kwargs["service_name"]
        self.ephemeral = kwargs.get("ephemeral") if isinstance(kwargs.get("ephemeral"), bool) else True
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.access_token = ""
        self.metadata = {"beat": "true"}
        self.heart_beat = kwargs.get("heartbeat_interval") or 5

    def get_server_addr(self):
        return random.sample(self.server_addrs, 1)[0]

    def send_request(self, method, url, params=None, body=None):
        """
        发送http请求，与nacos通信
        :param method: http method
        :param url: http url
        :param params: http query 参数
        :param body: http body 参数
        :return: http response
        """
        for i in range(5):
            try:
                resp = requests.request(method, url, params=params, json=body)
            except Exception as err:
                logger.error(err)
                continue
            else:
                if resp is None:
                    logger.info("请求返回为空，-> {}次continue".format(i + 1))
                    continue
                if resp.status_code == 403:
                    self.get_access_token()
                    if "accessToken" in params:
                        params.update(accessToken=self.access_token)
                    continue
                return resp

    def get_access_token(self):
        """
        申请nacos授权token
        :return: accessToken
        """
        url = "http://{}/nacos/v1/auth/login".format(self.get_server_addr())
        params = dict(
            username=self.username,
            password=self.password
        )
        resp = self.send_request(method="POST", url=url, params=params, body=params)
        if resp.status_code == 200:
            data = json.loads(resp.text)
            logger.info("获取token成功->" + str(data))
            self.access_token = data.get("accessToken")
            return data.get("accessToken")
        else:
            logger.info("获取token失败->" + str(resp) + resp.text)

    def send_heartbeat(self):
        """
        发送心跳检索机制，第一次心跳检测等同于服务注册
        """
        url = "http://{}/nacos/v1/ns/instance/beat".format(self.get_server_addr())
        beat_data = {
            "serviceName": self.service_name,
            "ip": self.ip,
            "port": self.port,
            "weight": 1,
            "ephemeral": self.ephemeral,
            "metadata": self.metadata  # 必填
        }
        params = dict(
            serviceName=self.service_name,
            groupName=self.group_name,
            ephemeral=self.ephemeral,
            beat=json.dumps(beat_data),
            accessToken=self.access_token,
            namespaceId=self.namespace
        )
        resp = self.send_request("PUT", url, params)
        if resp.status_code == 200:
            logger.info("heartbeat success" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        elif resp.status_code == 403:
            self.access_token = self.get_access_token()
            logger.info("heartbeat auth failed" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            logger.info("heartbeat failed" + str(resp) + resp.text)

    def async_handle(self):
        """
        线程异步处理心跳检测，与gunicorn子进程不堵塞，需要gunicorn预加载app，添加--preload启动参数
        :return:
        """
        def run():
            while True:
                try:
                    self.send_heartbeat()
                except Exception as err:
                    logger.info("send_hearbeat 失败, {}s后重试，{}".format(self.heart_beat, err))
                time.sleep(self.heart_beat)

        self.access_token = self.get_access_token()
        import threading
        thread = threading.Thread(target=run)
        thread.setDaemon(True)
        thread.start()

    def with_nacos_sdk(self):
        import nacos
        client = nacos.NacosClient(self.get_server_addr(),
                                   namespace=self.namespace,
                                   username=self.username,
                                   password=self.password)

        def run():
            while True:
                t = client.send_heartbeat(service_name=self.service_name,
                                          ip=self.ip,
                                          port=self.port,
                                          group_name=self.group_name,
                                          metadata=json.dumps({"beat": "true"}))
        from concurrent.futures import ThreadPoolExecutor
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(run)
