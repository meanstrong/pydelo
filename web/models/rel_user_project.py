#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from web import db
from web.utils.jsonencoder import JsonSerializer

__author__ = 'Rocky Peng'


class RelUserProject(JsonSerializer, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    user = db.relationship("Users",
                           backref=db.backref("projects", lazy="dynamic"))
    project = db.relationship("Projects",
                              backref=db.backref("users", lazy="dynamic"))
