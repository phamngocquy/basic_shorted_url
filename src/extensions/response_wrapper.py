# coding=utf-8
import logging

__author__ = 'QuyPN'
_logger = logging.getLogger(__name__)


def wrap_response(data=None, message="", error_code=0, metadata=None, msg_code=None):
    """ Return general HTTP response
    :param data:
    :param metadata:
    :param str message: detail info
    :param int error_code:
    :param str msg_code: code of message
    :return:
    """
    res = {
        'error_code': error_code,
        'success': error_code == 0,
        'message': message,
        'msg_code': msg_code
    }

    if data is not None:
        res['data'] = data
    if metadata:
        res['metadata'] = metadata
    return res
