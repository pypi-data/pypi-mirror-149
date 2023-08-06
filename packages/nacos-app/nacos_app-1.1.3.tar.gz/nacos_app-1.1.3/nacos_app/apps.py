# -*- coding: utf-8 -*-
# @Time    : 2021/12/8 11:39
# @Author  : xuyiqing
# @FileName: apps.py
import logging

from django.apps import AppConfig
from django.conf import settings

from nacos_app.balanced import LoadBalanced


logger = logging.getLogger("nacos")
if not logger.handlers:
    logger = logging.getLogger("django")

if getattr(settings, "NACOS_SERVER_DISCOVERY", None) is not None:
    loadbalanced = LoadBalanced(**settings.NACOS_SERVER_DISCOVERY)


class NacosRegisterConfig(AppConfig):

    name = "nacos_app"

    def ready(self):
        if getattr(settings, "NACOS_SERVER_DISCOVERY", None) is not None:
            loadbalanced.async_handle()
