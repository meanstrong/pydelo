#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.jsonencoder import JsonSerializer
class RelUserHost():
    pass


# class RelUserHost(JsonSerializer, db.Model):
# 
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"))
#     created_at = db.Column(db.DateTime, default=db.func.now())
#     updated_at= db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
# 
#     user = db.relationship("Users", backref=db.backref("hosts", lazy="dynamic"))
#     host = db.relationship("Hosts", backref=db.backref("users", lazy="dynamic"))
