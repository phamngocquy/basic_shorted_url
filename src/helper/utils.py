# coding=utf-8
import logging
import string
import random

from src.core.config import settings

__author__ = 'qPham'
_logger = logging.getLogger(__name__)


def random_shorten_url():
    token = ''.join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for _ in range(settings.LENGTH_SHORTEN_TOKEN)
    )
    return token


def get_remote_ip(req):
    ip: str = req.client.host
    if ip in ['127.0.0.1', 'localhost', settings.PROXY_IP]:
        if req.headers.get('X-Real-Ip'):
            ip = req.headers.get('X-Real-Ip')
        if ip.startswith("10."):
            if req.headers.get('X-Forwarded-For'):
                ip = req.headers.get('X-Forwarded-For')
                if ip and ", " in ip:
                    ip = ip.split(", ")[0]
    return ip
