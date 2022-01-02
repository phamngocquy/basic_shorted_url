# coding=utf-8
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

__author__ = 'qPham'

_logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)
