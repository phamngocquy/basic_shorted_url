# coding=utf-8
import logging

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from src.core.limiter import limiter
from src.cache import redis
from src.db import db_engine
from src.dbiz import dbiz_shorten_url

__author__ = 'qPham'

_logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/{shorten_token}', status_code=302)
@limiter.limit('30/minute')
async def redirect_url(
        *, db: Session = Depends(db_engine.get_db),
        request: Request, shorten_token: str
):
    client = redis.client(request)
    origin_url = await dbiz_shorten_url.get_origin_url(
        db, client, shorten_token, request
    )
    return RedirectResponse(origin_url)
