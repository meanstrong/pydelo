# -*- coding:utf-8 -*-

from flask import render_template, jsonify

from web import app
from .login import authorize

__author__ = 'Rocky Peng'


@app.route("/projects", methods=["GET"])
@authorize
def projects():
    return render_template("projects.html")


@app.route("/projects/<int:id>", methods=["GET"])
@authorize
def detail(id):
    return render_template("project_detail.html")


@app.route("/project/create", methods=["GET"])
@authorize
def project_create():
    return render_template("project_create.html")
