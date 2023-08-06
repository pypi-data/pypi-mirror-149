# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 9:51
# @Author  : xuyiqing
# @FileName: util.py
import logging
import socket

import requests

logger = logging.getLogger("nacos")
if not logger.handlers:
    logger = logging.getLogger("django")


def get_innerip():
    s, ip = None, None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s is not None:
            s.close()
    logger.info("获取本机局域网ip->{}".format(ip))
    return ip
