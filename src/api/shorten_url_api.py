# coding=utf-8
import logging
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from src import schemas
from src.cache import redis
from src.core.limiter import limiter
from src.core.security import JWTBearer
from src.db import db_engine
from src.dbiz import dbiz_shorten_url
from src.extensions.response_wrapper import wrap_response

__author__ = 'qPham'
_logger = logging.getLogger(__name__)
router = APIRouter()


@router.post('/', dependencies=[Depends(JWTBearer())])
@limiter.limit('30/minute')
async def create_shorten(*, db: Session = Depends(db_engine.get_db), request: Request,
                         origin_url_obj: schemas.OriginURL):
    client = redis.client(request)
    shorten_url = await dbiz_shorten_url.create_shorten_url(
        db, request, client, origin_url_obj
    )
    return wrap_response(
        data={
            'shorten_url': shorten_url
        }
    )


@router.get('/user-statistic/{user_id}', dependencies=[Depends(JWTBearer())])
async def statistic_by_userid(
        *, db: Session = Depends(db_engine.get_db),
        user_id: int
):
    resp = await dbiz_shorten_url.statistic_by_userid(db, user_id)
    return wrap_response(data=resp)


@router.get('/url-statistic/{user_id}/{shorten_token}', dependencies=[Depends(JWTBearer())])
async def statistic_by_userid(
        *, db: Session = Depends(db_engine.get_db),
        user_id: int,
        shorten_token: str
):
    resp = await dbiz_shorten_url.statistic_by_shorten_url(db, user_id, shorten_token)
    return wrap_response(data=resp)
