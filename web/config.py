# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

# -- app config --
DEBUG = True

# -- mysql config --
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASS = "abc$#@!8008CBA"
DB_NAME = "pydelo"

# -- web app config --
DEBUG = True
SECRET_KEY = "secret-key"
SESSION_COOKIE_NAME = "pydelo"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SITE_COOKIE = "pydelo-ck"
