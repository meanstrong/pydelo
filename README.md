Pydelo - A Deploy Tool
======================
这是一个Python语言编写的自动化上线部署系统，只需做很少的配置就可以立即使用。
系统将整个发布过程分成两个部分：checkout 和 deploy
* checkout
此部分做代码的检出动作，并且在代码的检出前后可以分别做一些shell操作，如编译动作，配置文件修改等。
* deploy
此部分做代码的发布动作，通过rsync将代码同步到远端机器的指定目录，在代码的同步前后也可以分别做一些shell操作，如相关服务的stop、start，某些清理工作等。

Requirements
------------

* Bash(git, rsync, ssh, sshpass)
* MySQL
* Python
* Python site-package(flask, flask-sqlalchemy, pymysql, paramiko)

That's all.

Installation
------------
```
apt-get install rsync sshpass
git clone git@github.com:meanstrong/pydelo.git
cd pydelo
pip install -r pip_requirements.txt # 建议使用virtualenv来部署
mysql -h root -p pydelo < db-schema.sql  # create database and tables
vi web/config.py # set up module config such as mysql connector
python init.py   # add some data to mysql or you can do it yourself

python manage.py # start flask web app
```

Usage
-----
#### 1.Add project
![image](https://github.com/meanstrong/pydelo/raw/master/docs/create_project.png)

#### 2.New deploy
![image](https://github.com/meanstrong/pydelo/raw/master/docs/create_deploy.png)

#### 3.Deploy progress
![image](https://github.com/meanstrong/pydelo/raw/master/docs/deploy_progress.png)

#### 4.Deploys
![image](https://github.com/meanstrong/pydelo/raw/master/docs/deploys.png)

Discussing
----------
- email: pmq2008@gmail.com
