# -*- coding:utf-8 -*-
from flask import render_template

from web import app
from .login import authorize

__author__ = 'Rocky Peng'


@app.route("/users", methods=["GET"])
@authorize
def users():
    return render_template("users.html")


@app.route("/users/<int:id>", methods=["GET"])
@authorize
def users_id(id):
    return render_template("host_detail.html")


@app.route("/users/create", methods=["GET"])
@authorize
def users_creation():
    return render_template("user_create.html")


@app.route("/users/<int:id>/hosts", methods=["GET"])
@authorize
def users_hosts(id):
    return render_template("user_hosts.html")


@app.route("/users/<int:id>/projects", methods=["GET"])
@authorize
def users_projects(id):
    return render_template("user_projects.html")
