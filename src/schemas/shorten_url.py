# coding=utf-8
import logging
from pydantic import BaseModel, AnyUrl

__author__ = 'qPham'
_logger = logging.getLogger(__name__)


class ShortenUrl(BaseModel):
    raw_url: str


class OriginURL(BaseModel):
    url: AnyUrl
    user_id: int
