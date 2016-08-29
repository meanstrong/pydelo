#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

import os
import threading
from web import db
from web.utils.log import Logger
from web.models.deploys import Deploys

from .base import Base
from web.utils.git import Git
from web.utils.localshell import LocalShell
from web.utils.remoteshell import RemoteShell
from web.utils.error import Error
import web.config as config

logger = Logger("deploy service")


class DeploysService(Base):
    __model__ = Deploys

    def deploy(self, deploy):
        if self.find(limit=1, status=2, project_id=deploy.project_id):
            logger.debug("deploy thread wait in quene")
            return
        t = threading.Thread(target=deploy_thread, args=(self, ), name="pydelo-deploy[%d]" % deploy.id)
        # TODO 当我不使用下面的语句时，project和host貌似在线程里面会没有值，也许我要把lazy值设置成select或者其他
        a = deploy.project, deploy.host
        t.start()

    def rollback(self, deploy):
        if self.find(limit=1, status=2, project_id=deploy.project_id):
            logger.debug("deploy thread wait in quene")
            return
        t = threading.Thread(target=rollback_thread, args=(self, ), name="pydelo-deploy[%d]" % deploy.id)
        # TODO 当我不使用下面的语句时，project和host貌似在线程里面会没有值，也许我要把lazy值设置成select或者其他
        a = deploy.project, deploy.host
        t.start()

    def build(self, deploy):
        t = threading.Thread(target=build_thread, args=(deploy,))
        # TODO 当我不使用下面的语句时，project和host貌似在线程里面会没有值，也许我要把lazy值设置成select或者其他
        a = deploy.project, deploy.host
        t.start()

    def append_comment(self, deploy, comment):
        sql = ("UPDATE {table} SET comment = CONCAT(comment, :comment) where id = {id}").format(
                table=self.__model__.__tablename__,
                id=deploy.id
                )
        db.session.execute(sql, {"comment": comment})
        db.session.commit()

deploys = DeploysService()

def rollback_thread(service):
    deploy = service.first(status=3)
    logger.info("deploy thread start: %d" % deploy.id)
    ssh = RemoteShell(host=deploy.host.ssh_host,
                      port=deploy.host.ssh_port,
                      user=deploy.host.ssh_user,
                      passwd=deploy.host.ssh_pass)

    try:
        # before rollback
        service.append_comment(deploy, "before rollback:\n")
        logger.debug("before rollback:")
        before_deploy = deploy.project.before_deploy.replace("\r", "").replace("\n", " && ")
        if before_deploy:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, before_deploy))
            if rc:
                raise Error(11000)
        service.append_comment(deploy, "OK!\n")
        service.update(deploy, progress=33)
        # rollback
        service.append_comment(deploy, "rollback:\n")
        logger.debug("rollback:")
        rc,stdout, stderr = ssh.exec_command("ln -snf {0} {1}".format(
            os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename), deploy.project.deploy_dir))
        if rc:
            raise Error(11001)
        service.append_comment(deploy, "OK!\n")
        service.update(deploy, progress=67)

        # after rollback
        service.append_comment(deploy, "after rollback:\n")
        logger.debug("after rollback:")
        after_deploy = deploy.project.after_deploy.replace("\r", "").replace("\n", " && ")
        if after_deploy:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, after_deploy))
            if rc:
                raise Error(11002)
        service.append_comment(deploy, "OK!\n")
    except Exception as err:
        service.append_comment(deploy, "Command: "+err.cmd+"\nReturn code: "+str(err.returncode)+"\nOutput: "+err.output)
        service.update(deploy, status=0)
    else:
        service.update(deploy, progress=100, status=1)
    finally:
        logger.info("deploy thread end: %d" % deploy.id)
        ssh.close()
        if service.find(limit=1, status=3, project_id=deploy.project_id):
            rollback_thread(service)

def deploy_thread(service):
    deploy = service.first(status=3)
    logger.info("deploy thread start: %d" % deploy.id)
    ssh = RemoteShell(host=deploy.host.ssh_host,
                      port=deploy.host.ssh_port,
                      user=deploy.host.ssh_user,
                      passwd=deploy.host.ssh_pass)
    try:
        service.update(deploy, progress=0, status=2)
        # before checkout
        git = Git(deploy.project.checkout_dir, deploy.project.repo_url)
        before_checkout = deploy.project.before_checkout.replace("\r", "").replace("\n", " && ")
        logger.debug("before_checkout"+before_checkout)
        service.append_comment(deploy, "before checkout:\n")
        cmd = "mkdir -p {0} && rm -rf {1}/*".format(
                deploy.project.target_dir, deploy.project.target_dir)
        LocalShell.check_call(cmd, shell=True)
        if before_checkout:
            cmd = "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.checkout_dir, before_checkout)
            LocalShell.check_call(cmd, shell=True)
        service.append_comment(deploy, "OK!\n")
        service.update(deploy, progress=17)
        # checkout
        service.append_comment(deploy, "checkout:\n")
        git.clone()
        if deploy.mode == 0:
            git.checkout_branch(deploy.branch, deploy.version)
        else:
            git.checkout_tag(deploy.version)
        service.append_comment(deploy, "OK!\n")
        service.update(deploy, progress=33)
        # after checkout
        after_checkout = deploy.project.after_checkout.replace("\r", "").replace("\n", " && ")
        service.append_comment(deploy, "after checkout:\n")
        if after_checkout:
            cmd = "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.checkout_dir, after_checkout)
            LocalShell.check_call(cmd, shell=True)
        service.append_comment(deploy, "OK!\n")
        service.update(deploy, progress=50)
        # before deploy
        service.append_comment(deploy, "before deploy:\n")
        ssh.check_call(
            "mkdir -p {0}".format(
                os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename)))

        logger.debug("before deploy:")
        ssh.check_call(
            "WORKSPACE='{0}' && cd $WORKSPACE && ls -1t | tail -n +{1} | xargs rm -rf".format(
                deploy.project.deploy_history_dir, config.MAX_DEPLOY_HISTORY))
        before_deploy = deploy.project.before_deploy.replace("\r", "").replace("\n", " && ")
        if before_deploy:
            ssh.check_call(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, before_deploy))
        service.append_comment(deploy, "OK!\n")
        service.update(deploy, progress=67)
        # deploy
        service.append_comment(deploy, "deploy:\n")
        logger.debug("deploy:")
        logger.debug("rsync:")
        cmd = ("rsync -avzq --rsh=\"sshpass -p {ssh_pass} ssh -p {ssh_port}\" --exclude='.git' {local_dest}/ {ssh_user}@{ssh_host}:{remote_dest}/").format(
            local_dest=deploy.project.target_dir,
            remote_dest=os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename),
            ssh_user=deploy.host.ssh_user,
            ssh_host=deploy.host.ssh_host,
            ssh_port=deploy.host.ssh_port,
            ssh_pass=deploy.host.ssh_pass)
        LocalShell.check_call(cmd, shell=True)
        ssh.check_call("ln -snf {0} {1}".format(
            os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename), deploy.project.deploy_dir))
        service.append_comment(deploy, "OK!\n")
        service.update(deploy, progress=83)

        # after deploy
        service.append_comment(deploy, "after deploy:\n")
        logger.debug("after deploy:")
        after_deploy = deploy.project.after_deploy.replace("\r", "").replace("\n", " && ")
        if after_deploy:
            ssh.check_call(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, after_deploy))
        service.append_comment(deploy, "OK!\n")
    except Exception as err:
        logger.error(err)
        service.append_comment(deploy, "Command: "+err.cmd+"\nReturn code: "+str(err.returncode)+"\nOutput: "+err.output)
        service.update(deploy, status=0)
    else:
        service.update(deploy, progress=100, status=1)
    finally:
        logger.info("deploy thread end: %d" % deploy.id)
        ssh.close()
        if service.find(limit=1, status=3, project_id=deploy.project_id):
            deploy_thread(service)

def build_thread(deploy):
    # before checkout
    git = Git(deploy.project.checkout_dir, deploy.project.repo_url)
    before_checkout = deploy.project.before_checkout.replace("\r", "").replace("\n", " && ")
    logger.debug("before_checkout"+before_checkout)
    if before_checkout:
        LocalShell.check_call(
            "WORKSPACE='{0}' && mkdir -p $WORKSPACE && cd $WORKSPACE && {1}".format(
                deploy.project.checkout_dir, before_checkout),
            shell=True)
    # checkout
    git.clone()
    if deploy.mode == 0:
        git.checkout_branch(deploy.branch, deploy.version)
    else:
        git.checkout_tag(deploy.version)
    # after checkout
    after_checkout = deploy.project.after_checkout.replace("\r", "").replace("\n", " && ")
    if after_checkout:
        LocalShell.check_call(
            "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                deploy.project.checkout_dir, after_checkout),
            shell=True)
