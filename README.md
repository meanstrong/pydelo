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

Usage
-----
#### 1.Add project
![image](https://github.com/meanstrong/pydelo/master/docs/create_project.png)

#### 2.New deploy
![image](https://github.com/meanstrong/pydelo/master/docs/create_deploy.png)

#### 3.Deploy progress
![image](https://github.com/meanstrong/pydelo/master/docs/deploy_progress.png)

#### 4.Deploys
![image](https://github.com/meanstrong/pydelo/master/docs/deploys.png)

Discussing
----------
- email: pmq2008@gmail.com
