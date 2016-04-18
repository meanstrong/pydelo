Pydelo - A Deploy Tool
======================
这是一个Python语言编写的自动化发布系统，只需做很少的配置就可以立即使用。

Requirements
------------

* Bash(git, ssh, sshpass)
* MySQL
* Python
* Python site-package(flask, flask-sqlalchemy, pymysql, paramiko)
That's all.

Installation
------------
```
git clone git@github.com:meanstrong/pydelo.git
cd pydelo
mysql -h root -p pydelo < db-schema.sql  # create database
vi web/config.py # set up module config such as mysql connector
python init.py   # init some sql data 
```

Discussing
----------
- email: pmq2008@gmail.com
