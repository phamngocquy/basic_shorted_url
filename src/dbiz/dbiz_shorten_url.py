# coding=utf-8
import asyncio
import logging

from fastapi import HTTPException
from urllib.parse import urlparse
from src.core.config import settings
from src.helper import utils
from src.models import ShortenUrl
from src.models.url_click import URLClick

__author__ = 'qPham'
_logger = logging.getLogger(__name__)


async def get_origin_url(db, redis, shorten_token, request):
    origin_url = await redis.get(shorten_token)
    try:
        if not origin_url:
            origin_url = ShortenUrl.first_by_or_error(
                db, shorten_token=shorten_token
            ).origin_url
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Shorten URL not exist"
        )
    # asyncio.get_event_loop().run_in_executor(
    #     request.app.state.executor,
    #     update_url_statistic,
    #     db,
    #     shorten_token,
    #     request
    # )
    await update_url_statistic(db, shorten_token, request)
    return origin_url


async def update_url_statistic(db, shorten_token, request):
    obj = ShortenUrl.first_by(db, shorten_token=shorten_token)
    obj.update(db, data={
        'number_click': obj.number_click + 1
    }, commit=True)

    URLClick.create(db, {
        'shorten_token': shorten_token,
        'ip': utils.get_remote_ip(request),
        'referer': request.headers.get('referer'),
        'user_agent': request.headers.get('user-agent')
    }, commit=True)


async def create_shorten_url(db, request, redis, origin_url_obj):
    """
    :param db:
    :param request
    :param redis:
    :param origin_url_obj:
    :return:
    """
    token = utils.random_shorten_url()
    domain = urlparse(request.headers.get('referer')).netloc
    while ShortenUrl.first_by(db, shorten_token=token):
        token = utils.random_shorten_url()
        _logger.warning(' Duplicated shorten token')

    obj = ShortenUrl.create(db, {
        'user_id': origin_url_obj.user_id,
        'origin_url': origin_url_obj.url,
        'shorten_token': token,
        'source': domain
    }, commit=True)
    await redis.set(token, origin_url_obj.url)
    return f'https://{settings.DOMAIN_NAME}/{obj.shorten_token}'


async def statistic_by_userid(db, user_id):
    shorten_objs = ShortenUrl.query_by(db, user_id=user_id)
    return shorten_objs


async def statistic_by_shorten_url(db, user_id, shorten_token):
    shorten_url = ShortenUrl.first_by(
        db,
        user_id=user_id,
        shorten_token=shorten_token
    )
    if not shorten_url:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission on this shorten url"
        )
    url_click = URLClick.query_by(db, shorten_token=shorten_token)
    return url_click
