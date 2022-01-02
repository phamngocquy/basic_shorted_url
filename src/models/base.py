# coding=utf-8
import logging
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative

__author__ = 'qPham'

_logger = logging.getLogger(__name__)


@as_declarative()
class BaseModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(), default=datetime.now, nullable=False, onupdate=datetime.now)

    @classmethod
    def create(cls, session, data, commit=False):
        """
         Create new model object with given dict `data`
        :param session:
        :param data:
        :param commit:
        :return:
        """
        obj = cls(**data)
        session.add(obj)
        if commit:
            session.commit()
        else:
            session.flush()
        return obj

    def update(self, session, data, commit=False, exclude=None):
        """
        Update current model object with given dict `data`
        :param session:
        :param data: dict
        :param commit:
        :param exclude: list of key to exclude from `data` dict
        :return:
        """
        for key, value in data.items():
            if not exclude or key not in exclude:
                setattr(self, key, value)

        if commit:
            session.commit()
        else:
            session.flush()
        return self

    @classmethod
    def query_by(cls, session, **kwargs):
        res = session.query(cls).filter_by(**kwargs).all()
        return res

    @classmethod
    def first_by(cls, session, **kwargs):
        obj = session.query(cls).filter_by(**kwargs).first()
        return obj

    @classmethod
    def first_by_or_error(cls, session, **kwargs):
        obj = session.query(cls).filter_by(**kwargs).first()
        if not obj:
            raise Exception(f'Obj {cls.__name__} not found')
        return obj
