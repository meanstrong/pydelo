# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web.utils.log import Logger

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from web.utils.jsonencoder import JSONEncoder

app = Flask(__name__)
app.config.from_object("web.config")
Logger.DEBUG_MODE = app.config["DEBUG"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(
    app.config["DB_USER"], app.config["DB_PASS"], app.config["DB_HOST"], app.config["DB_NAME"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.json_encoder = JSONEncoder
db = SQLAlchemy(app)

from .controller import api, webhooks, login, deploys, project, host, users
