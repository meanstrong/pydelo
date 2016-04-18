# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from flask import render_template

from web import app
from .login import authorize

@app.route("/deploys", methods=["GET"])
@authorize
def deploys():
    return render_template("deploys.html")

@app.route("/deploy/create", methods=["GET"])
@authorize
def deploys_new():
    return render_template("deploy_create.html")
