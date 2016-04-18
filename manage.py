# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import app

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9998, debug=app.config["DEBUG"])
