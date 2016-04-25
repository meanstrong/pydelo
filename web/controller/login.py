# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

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
def authorize(func):
    @wraps(func)
    def decorator(*args, **kargs):
        apikey = request.args.get("apikey")
        sign = request.cookies.get('sign')
        if users.is_login(sign, apikey):
            g.user = users.first(apikey=apikey) or users.get(sessions.first(session=sign).user_id)
            if g.user is not None:
                return func(*args, **kargs)
        return redirect(url_for('login', next=request.path))
    return decorator

#login_manager = LoginManager()
#login_manager.init_app(app)
#
#@login_manager.request_loader
#def load_user(request):
#    apikey = request.args.get("apikey")
#    if apikey:
#        return users.first(apikey=apikey)
#    sign = request.cookies.get('sign')
#    if sign and User.is_session_validate(sign):
#        return User.get_by_session(sign)
#    return None
#
#login_manager.login_view = "/login"

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

# @app.route("/login", methods=["POST"])
# def to_login():
#     logger.debug("POST /login")
#     username = request.form.get("username")
#     password = request.form.get("password")
#     user = User(username)
#     if not user.is_exist(username):
#         return render_template("login.html")
#     if not user.is_password_correct(password):
#         return render_template("login.html")
#     session = ''.join(random.choice(string.letters+string.digits) for _ in range(20))
#     user.update_session(session)
#     response = redirect(url_for('deploys'))
#     response.set_cookie(key='sign', value=session, max_age=7 * 24 * 60 * 60)
#     return response

@app.route("/logout")
@authorize
def logout():
    users.logout(g.user)
    resp = redirect(url_for('login'))
    resp.set_cookie("sign", "", expires=0)
    return resp
