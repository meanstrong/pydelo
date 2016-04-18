#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db


class Base(object):
    __model__ = None

    def save(self, model):
        db.session.add(model)
        db.session.commit()
        return model
    
    def find(self, offset=None, limit=None, order_by=None, desc=False, **kargs):
        query = self.__model__.query.filter_by(**kargs)
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

    def first(self, **kargs):
        return self.__model__.query.filter_by(**kargs).first()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_or_404(self, id):
        self.__model__.query.get_or_404(id)

    def count(self, **kargs):
        return self.__model__.query.filter_by(**kargs).count()

    def all(self, offset=None, limit=None, order_by=None, desc=False):
        query = self.__model__.query
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
        for k,v in kargs.items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        db.session.delete(model)
        db.session.commit()
