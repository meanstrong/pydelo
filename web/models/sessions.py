#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from web import db
from web.utils.jsonencoder import JsonSerializer

__author__ = 'Rocky Peng'


class Sessions(JsonSerializer, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    session = db.Column(db.String(32))
    expired = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    user = db.relationship("Users",
                           backref=db.backref("sessions", lazy="dynamic"))
