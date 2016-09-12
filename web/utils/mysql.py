import MySQLdb
import pymysql
import config

from log import Logger
logger = Logger("web.utils.mysql")


class PyMySQL(object):
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

        self.connect()
        self.conn.autocommit(1)
        self.cursor = self.conn.cursor()

    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset="utf8")

sql_conn = PyMySQL(
        host=config.DB_HOST,
        user=config.DB_USER,
        passwd=config.DB_PASS,
        port=config.DB_PORT,
        db=config.DB_NAME)
