#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from web import db
from web.utils.jsonencoder import JsonSerializer

__author__ = 'Rocky Peng'


class Deploys(JsonSerializer, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"))
    mode = db.Column(db.Integer)
    branch = db.Column(db.String(32))
    version = db.Column(db.String(32))
    progress = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)
    softln_filename = db.Column(db.String(64))
    comment = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    user = db.relationship("Users",
                           backref=db.backref("deploys", lazy="dynamic"))
    project = db.relationship("Projects",
                              backref=db.backref("deploys", lazy="dynamic"))
    host = db.relationship("Hosts",
                           backref=db.backref("deploys", lazy="dynamic"))
