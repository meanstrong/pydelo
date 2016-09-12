# -*- coding:utf-8 -*-
from flask import render_template

from web import app
from .login import authorize

__author__ = 'Rocky Peng'


@app.route("/deploys", methods=["GET"])
@authorize
def deploys():
    return render_template("deploys.html")


@app.route("/deploy/create", methods=["GET"])
@authorize
def deploys_new():
    return render_template("deploy_create.html")


@app.route("/deploys/<int:id>/progress", methods=["GET"])
@authorize
def deploy_progress(id):
    return render_template("deploy_progress.html")
