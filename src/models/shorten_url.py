# coding=utf-8
import logging
from sqlalchemy import Column, VARCHAR, Integer, DateTime
from src.models.base import BaseModel

__author__ = 'qPham'
_logger = logging.getLogger(__name__)


class ShortenUrl(BaseModel):
    __tablename__ = 'shorten_url'
    user_id = Column(Integer, nullable=False)
    origin_url = Column(VARCHAR(255), nullable=False, index=True)
    shorten_token = Column(VARCHAR(8), nullable=False, unique=True)
    number_click = Column(Integer, nullable=False, default=0)
    expire_time = Column(DateTime())
    source = Column(VARCHAR(255), nullable=False)
