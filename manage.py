# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import app

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=app.config["PORT"], debug=app.config["DEBUG"])
