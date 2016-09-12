# -*- coding:utf-8 -*-
from web import app

__author__ = 'Rocky Peng'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=app.config["DEBUG"])
