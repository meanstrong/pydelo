#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from web import db
from web.utils.jsonencoder import JsonSerializer

__author__ = 'Rocky Peng'


rel_user_project = db.Table(
    "rel_user_project",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id")),
    db.Column("created_at", db.DateTime, default=db.func.now()),
    db.Column("updated_at", db.DateTime, default=db.func.now(),
              onupdate=db.func.now()),
)


class Projects(JsonSerializer, db.Model):
    __json_hidden__ = ["deploys", "users"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    repo_url = db.Column(db.String(200))
    checkout_dir = db.Column(db.String(200))
    target_dir = db.Column(db.String(200))
    deploy_dir = db.Column(db.String(200))
    deploy_history_dir = db.Column(db.String(200))
    before_checkout = db.Column(db.Text, default="")
    after_checkout = db.Column(db.Text, default="")
    before_deploy = db.Column(db.Text, default="")
    after_deploy = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now())

    users = db.relationship("Users", secondary=rel_user_project,
                            backref=db.backref("projects", lazy="dynamic"))
