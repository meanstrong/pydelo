# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from flask import render_template

from web import app
from .login import authorize

@app.route("/hosts", methods=["GET"])
@authorize
def hosts():
    return render_template("hosts.html")

@app.route("/hosts/<int:id>", methods=["GET"])
@authorize
def hosts_id(id):
    return render_template("host_detail.html")

@app.route("/host/create", methods=["GET"])
@authorize
def host_creation():
    return render_template("host_create.html")

@app.route("/host/<int:id>/group", methods=["GET"])
@authorize
def host_group(id):
    return render_template("host_detail.html")
