# coding=utf-8
import logging
from fastapi import APIRouter
from src.api import shorten_url_api, redirect_url_api

__author__ = 'qPham'
_logger = logging.getLogger(__name__)

api_router = APIRouter()
api_router.include_router(
    shorten_url_api.router,
    prefix="/shorten-url",
    tags=["shorten"]
)

api_router.include_router(
    redirect_url_api.router,
    prefix='',
    tags=['shorten']
)
