#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.jsonencoder import JsonSerializer


class Users(JsonSerializer, db.Model):
    __json_hidden__ = ["deploys", "sessions", "hosts", "projects"]

    ROLE = dict(ADMIN=1, NORMAL=2)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(64))
    role = db.Column(db.Integer, default=2)
    email = db.Column(db.String(64))
    phone = db.Column(db.String(16))
    apikey = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at= db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
