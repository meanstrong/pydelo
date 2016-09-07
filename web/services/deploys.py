#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

import traceback
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

logger = Logger("web.deploys.deploys")


class DeploysService(Base):
    __model__ = Deploys

    def deploy(self, deploy):
        if self.count(status=2, project_id=deploy.project_id):
            logger.debug("deploy thread wait in quene")
            return
        first_deploy = self.first(status=3, project_id=deploy.project_id)
        if first_deploy.mode == 0 or first_deploy.mode == 1:
            t = threading.Thread(target=deploy_thread,
                                 args=(deploy.project_id,),
                                 name="pydelo-deploy[%d]" % deploy.id)
            t.start()
        elif first_deploy.mode == 2:
            t = threading.Thread(target=rollback_thread,
                                 args=(deploy.project_id,),
                                 name="pydelo-deploy[%d]" % deploy.id)
            t.start()

    def rollback(self, deploy):
        if self.find(status=2, project_id=deploy.project_id).count():
            logger.debug("deploy thread wait in quene")
            return
        t = threading.Thread(target=rollback_thread, args=(deploy.project_id,),
                             name="pydelo-deploy[%d]" % deploy.id)
        t.start()

    def append_comment(self, deploy, comment):
        sql = ("UPDATE {table} SET comment = CONCAT(comment, :comment) where "
               "id = {id}").format(table=self.__model__.__tablename__,
                                   id=deploy.id)
        self.session.execute(sql, {"comment": comment})
        self.session.commit()

deploys = DeploysService()

def rollback_thread(project_id):
    deploys = DeploysService()
    deploy = deploys.first(project_id=project_id, status=3)
    logger.info("deploy thread start: %d" % deploy.id)
    ssh = RemoteShell(host=deploy.host.ssh_host,
                      port=deploy.host.ssh_port,
                      user=deploy.host.ssh_user,
                      passwd=deploy.host.ssh_pass)
    try:
        # before rollback
        deploys.append_comment(deploy, "before rollback:\n")
        logger.debug("before rollback:")
        before_deploy = deploy.project.before_deploy.replace("\r", "").replace(
            "\n", " && ")
        if before_deploy:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, before_deploy))
            if rc:
                raise Error(11000)
        deploys.append_comment(deploy, "OK!\n")
        deploys.update(deploy, progress=33)
        # rollback
        deploys.append_comment(deploy, "rollback:\n")
        logger.debug("rollback:")
        rc,stdout, stderr = ssh.exec_command("ln -snf {0} {1}".format(
            os.path.join(deploy.project.deploy_history_dir,
                         deploy.softln_filename),
            deploy.project.deploy_dir))
        if rc:
            raise Error(11001)
        deploys.append_comment(deploy, "OK!\n")
        deploys.update(deploy, progress=67)

        # after rollback
        deploys.append_comment(deploy, "after rollback:\n")
        logger.debug("after rollback:")
        after_deploy = deploy.project.after_deploy.replace("\r", "").replace(
            "\n", " && ")
        if after_deploy:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, after_deploy))
            if rc:
                raise Error(11002)
        deploys.append_comment(deploy, "OK!\n")
    except Exception as err:
        traceback.print_exc()
        deploys.append_comment(deploy, repr(err))
                               # ("Command: "+err.cmd+"\nReturn code: "+
                               #  str(err.returncode)+"\nOutput: "+err.output))
        deploys.update(deploy, status=0)
    else:
        deploys.update(deploy, progress=100, status=1)
    finally:
        logger.info("deploy thread end: %d" % deploy.id)
        ssh.close()
        deploy = deploys.first(project_id=deploy.project_id, status=3)
        if deploy:
            deploys.deploy(deploy)

def deploy_thread(project_id):
    deploys = DeploysService()
    deploy = deploys.first(project_id=project_id, status=3)
    if not deploy:
        logger.info("no deploy wait in quene.")
        return
    logger.info("deploy thread start: {}".format(deploy.id))
    ssh = RemoteShell(host=deploy.host.ssh_host,
                      port=deploy.host.ssh_port,
                      user=deploy.host.ssh_user,
                      passwd=deploy.host.ssh_pass)
    try:
        deploys.update(deploy, progress=0, status=2)
        # before checkout
        git = Git(deploy.project.checkout_dir, deploy.project.repo_url)
        before_checkout = deploy.project.before_checkout.replace(
            "\r", "").replace("\n", " && ")
        logger.debug("before_checkout"+before_checkout)
        deploys.append_comment(deploy, "before checkout:\n")
        cmd = "mkdir -p {0} && rm -rf {1}/*".format(
                deploy.project.target_dir, deploy.project.target_dir)
        LocalShell.check_call(cmd, shell=True)
        if before_checkout:
            cmd = "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.checkout_dir, before_checkout)
            LocalShell.check_call(cmd, shell=True)
        deploys.append_comment(deploy, "OK!\n")
        deploys.update(deploy, progress=17)
        # checkout
        deploys.append_comment(deploy, "checkout:\n")
        git.clone()
        if deploy.mode == 0:
            git.checkout_branch(deploy.branch, deploy.version)
        else:
            git.checkout_tag(deploy.version)
        deploys.append_comment(deploy, "OK!\n")
        deploys.update(deploy, progress=33)
        # after checkout
        after_checkout = deploy.project.after_checkout.replace(
            "\r", "").replace("\n", " && ")
        deploys.append_comment(deploy, "after checkout:\n")
        if after_checkout:
            cmd = "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.checkout_dir, after_checkout)
            LocalShell.check_call(cmd, shell=True)
        deploys.append_comment(deploy, "OK!\n")
        deploys.update(deploy, progress=50)
        # before deploy
        deploys.append_comment(deploy, "before deploy:\n")
        ssh.check_call(
            "mkdir -p {0}".format(
                os.path.join(deploy.project.deploy_history_dir,
                             deploy.softln_filename)))

        logger.debug("before deploy:")
        ssh.check_call(
            ("WORKSPACE='{0}' && cd $WORKSPACE && ls -1t | tail -n +{1} | "
             "xargs rm -rf").format(deploy.project.deploy_history_dir,
                                    config.MAX_DEPLOY_HISTORY))
        before_deploy = deploy.project.before_deploy.replace("\r", "").replace(
            "\n", " && ")
        if before_deploy:
            ssh.check_call(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, before_deploy))
        deploys.append_comment(deploy, "OK!\n")
        deploys.update(deploy, progress=67)
        # deploy
        deploys.append_comment(deploy, "deploy:\n")
        logger.debug("deploy:")
        logger.debug("rsync:")
        cmd = ("rsync -avzq --rsh=\"sshpass -p {ssh_pass} ssh -p {ssh_port}\" "
               "--exclude='.git' {local_dest}/ {ssh_user}@{ssh_host}:"
               "{remote_dest}/").format(local_dest=deploy.project.target_dir,
                                        remote_dest=os.path.join(
                                            deploy.project.deploy_history_dir,
                                            deploy.softln_filename),
                                        ssh_user=deploy.host.ssh_user,
                                        ssh_host=deploy.host.ssh_host,
                                        ssh_port=deploy.host.ssh_port,
                                        ssh_pass=deploy.host.ssh_pass)
        LocalShell.check_call(cmd, shell=True)
        ssh.check_call("ln -snf {0} {1}".format(
            os.path.join(deploy.project.deploy_history_dir,
                         deploy.softln_filename),
            deploy.project.deploy_dir))
        deploys.append_comment(deploy, "OK!\n")
        deploys.update(deploy, progress=83)

        # after deploy
        deploys.append_comment(deploy, "after deploy:\n")
        logger.debug("after deploy:")
        after_deploy = deploy.project.after_deploy.replace("\r", "").replace(
            "\n", " && ")
        if after_deploy:
            ssh.check_call(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, after_deploy))
        deploys.append_comment(deploy, "OK!\n")
    except Exception as err:
        traceback.print_exc()
        logger.error(err)
        deploys.append_comment(deploy, repr(err))
                               # ("Command: "+err.cmd+"\nReturn code: "+
                               #  str(err.returncode)+"\nOutput: "+err.output))
        deploys.update(deploy, status=0)
    else:
        deploys.update(deploy, progress=100, status=1)
    finally:
        logger.info("deploy thread end: %d" % deploy.id)
        ssh.close()
        deploy = deploys.first(project_id=project_id, status=3)
        if deploy:
            logger.info("deploy thread fetch from wait: {}".format(deploy))
            deploys.deploy(deploy)
