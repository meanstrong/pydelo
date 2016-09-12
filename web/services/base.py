#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from web import db
from web import db_session
from web.utils.log import Logger
logger = Logger("web.services.base")
__author__ = 'Rocky Peng'


class Base(object):
    __model__ = None

    def __init__(self, session=None):
        self.session = session or db_session

    def save(self, model):
        self.session.add(model)
        self.session.commit()
        return model

    def find(self, **kargs):
        query = self.session.query(self.__model__).filter_by(**kargs)
        return query

    def first(self, **kargs):
        return self.session.query(self.__model__).filter_by(**kargs).first()

    def get(self, id):
        self.session.expire_all()
        return self.session.query(self.__model__).get(id)

    def get_or_404(self, id):
        self.session.query(self.__model__).get_or_404(id)

    def count(self, **kargs):
        return self.session.query(self.__model__).filter_by(**kargs).count()

    def all(self, offset=None, limit=None, order_by=None, desc=False):
        query = self.session.query(self.__model__)
        if order_by is not None:
            if desc:
                query = query.order_by(db.desc(order_by))
            else:
                query = query.order_by(order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    def create(self, **kargs):
        return self.save(self.__model__(**kargs))

    def update(self, model, **kargs):
        for k, v in kargs.items():
            setattr(model, k, v)
        self.save(model)
        return model

    def session_commit(self):
        self.session.commit()

    def __del__(self):
        logger.info("session close.")
        self.session.close()
