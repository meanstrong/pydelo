#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.jsonencoder import JsonSerializer

rel_user_host = db.Table("rel_user_host",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("host_id", db.Integer, db.ForeignKey("hosts.id")),
    db.Column("created_at", db.DateTime, default=db.func.now()),
    db.Column("updated_at", db.DateTime, default=db.func.now(), onupdate=db.func.now()),
)


class Hosts(JsonSerializer, db.Model):
    __json_hidden__ = ["deploys", "users"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ssh_host = db.Column(db.String(32))
    ssh_port = db.Column(db.Integer)
    ssh_user = db.Column(db.String(64))
    ssh_method = db.Column(db.Integer())
    ssh_pass = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at= db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    users = db.relationship("Users", secondary=rel_user_host,
        backref=db.backref("hosts", lazy="dynamic"))
