# -*- coding:utf-8 -*-
import collections
from datetime import datetime
from hashlib import md5
import random
import string
from flask import request, Response, redirect, url_for, render_template, g

from web import app
from web.services.users import users
from web.services.sessions import sessions

from functools import wraps

__author__ = 'Rocky Peng'


def authorize(func):
    @wraps(func)
    def decorator(*args, **kargs):
        apikey = request.args.get("apikey")
        sign = request.cookies.get('sign')
        if users.is_login(sign, apikey):
            g.user = users.first(apikey=apikey) or \
                users.get(sessions.first(session=sign).user_id)
            if g.user is not None:
                return func(*args, **kargs)
        return redirect(url_for('login', next=request.path))
    return decorator


@app.route("/", methods=["GET"])
@authorize
def index():
    return redirect(url_for('deploys'))


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/account/change_password", methods=["GET"])
@authorize
def change_password():
    return render_template("account_change_password.html")


@app.route("/logout")
@authorize
def logout():
    users.logout(g.user)
    resp = redirect(url_for('login'))
    resp.set_cookie("sign", "", expires=0)
    return resp
