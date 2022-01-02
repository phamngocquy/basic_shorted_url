# coding=utf-8
import logging
from sqlalchemy import Column, VARCHAR, Integer, DateTime
from src.models.base import BaseModel

__author__ = 'qPham'
_logger = logging.getLogger(__name__)


class URLClick(BaseModel):
    __tablename__ = 'url_click'
    shorten_token = Column(VARCHAR(8), nullable=False)
    ip = Column(VARCHAR(55), nullable=False)
    user_agent = Column(VARCHAR(512))
    referer = Column(VARCHAR(512))
