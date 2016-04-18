# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from flask import request, Response, redirect, url_for, render_template, jsonify

from web import app
from .login import authorize

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
