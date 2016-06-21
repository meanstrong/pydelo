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
        t = threading.Thread(target=deploy_thread, args=(self, deploy))
        # TODO 当我不使用下面的语句时，project和host貌似在线程里面会没有值，也许我要把lazy值设置成select或者其他
        a = deploy.project, deploy.host
        t.start()

    def rollback(self, deploy):
        t = threading.Thread(target=rollback_thread, args=(self, deploy))
        # TODO 当我不使用下面的语句时，project和host貌似在线程里面会没有值，也许我要把lazy值设置成select或者其他
        a = deploy.project, deploy.host
        t.start()

    def build(self, deploy):
        t = threading.Thread(target=build_thread, args=(deploy,))
        # TODO 当我不使用下面的语句时，project和host貌似在线程里面会没有值，也许我要把lazy值设置成select或者其他
        a = deploy.project, deploy.host
        t.start()

deploys = DeploysService()

def rollback_thread(service, deploy):
    ssh = RemoteShell(host=deploy.host.ssh_host,
                      port=deploy.host.ssh_port,
                      user=deploy.host.ssh_user,
                      passwd=deploy.host.ssh_pass)

    try:
        # before rollback
        logger.debug("before rollback:")
        before_rollback = deploy.project.before_rollback.replace("\r", "").replace("\n", " && ")
        if before_rollback:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, before_rollback))
            if rc:
                raise Error(11000)
        service.update(deploy, progress=33)
        # rollback
        logger.debug("rollback:")
        rc,stdout, stderr = ssh.exec_command("ln -snf {0} {1}".format(
            os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename), deploy.project.deploy_dir))
        if rc:
            raise Error(11001)
        service.update(deploy, progress=67)

        # after rollback
        logger.debug("after rollback:")
        after_rollback = deploy.project.after_rollback.replace("\r", "").replace("\n", " && ")
        if after_rollback:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, after_rollback))
            if rc:
                raise Error(11002)
    except Exception:
        service.update(deploy, status=0)
    else:
        service.update(deploy, progress=100, status=1)
    finally:
        ssh.close()

def deploy_thread(service, deploy):
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
        if before_checkout:
            LocalShell.check_call(
                "WORKSPACE='{0}' && mkdir -p $WORKSPACE && cd $WORKSPACE && {1}".format(
                    deploy.project.checkout_dir, before_checkout),
                shell=True)
        service.update(deploy, progress=17)
        # checkout
        git.clone()
        if deploy.mode == 0:
            git.checkout(deploy.branch, deploy.version)
        else:
            git.checkout(tag=deploy.version)
        service.update(deploy, progress=33)
        # after checkout
        after_checkout = deploy.project.after_checkout.replace("\r", "").replace("\n", " && ")
        if after_checkout:
            LocalShell.check_call(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.checkout_dir, after_checkout),
                shell=True)
        service.update(deploy, progress=50)
        # before deploy
        rc, stdout, stderr = ssh.exec_command(
            "mkdir -p {0}".format(
                os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename)))
        if rc:
            raise Error(11003)

        logger.debug("before deploy:")
        rc, stdout, stderr = ssh.exec_command(
            "WORKSPACE='{0}' && cd $WORKSPACE && ls -1t | tail -n +{1} | xargs rm -rf".format(
                deploy.project.deploy_history_dir, config.MAX_DEPLOY_HISTORY))
        if rc:
            raise Error(11000)
        before_deploy = deploy.project.before_deploy.replace("\r", "").replace("\n", " && ")
        if before_deploy:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, before_deploy))
            if rc:
                raise Error(11000)
        service.update(deploy, progress=67)
        # deploy
        logger.debug("deploy:")
        logger.debug("rsync:")
        shell = ("rsync -avzq --rsh=\"sshpass -p {ssh_pass} ssh -p {ssh_port}\" --exclude='.git' {local_dest}/ {ssh_user}@{ssh_host}:{remote_dest}/").format(
            local_dest=deploy.project.checkout_dir,
            remote_dest=os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename),
            ssh_user=deploy.host.ssh_user,
            ssh_host=deploy.host.ssh_host,
            ssh_port=deploy.host.ssh_port,
            ssh_pass=deploy.host.ssh_pass)
        LocalShell.check_call(shell, shell=True)
        rc,stdout, stderr = ssh.exec_command("ln -snf {0} {1}".format(
            os.path.join(deploy.project.deploy_history_dir, deploy.softln_filename), deploy.project.deploy_dir))
        if rc:
            raise Error(11001)
        service.update(deploy, progress=83)

        # after deploy
        logger.debug("after deploy:")
        after_deploy = deploy.project.after_deploy.replace("\r", "").replace("\n", " && ")
        if after_deploy:
            rc, stdout, stderr = ssh.exec_command(
                "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                    deploy.project.deploy_dir, after_deploy))
            if rc:
                raise Error(11002)
    except Exception:
        service.update(deploy, status=0)
    else:
        service.update(deploy, progress=100, status=1)
    finally:
        ssh.close()

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
        git.checkout(deploy.branch, deploy.version)
    else:
        git.checkout(tag=deploy.version)
    # after checkout
    after_checkout = deploy.project.after_checkout.replace("\r", "").replace("\n", " && ")
    if after_checkout:
        LocalShell.check_call(
            "WORKSPACE='{0}' && cd $WORKSPACE && {1}".format(
                deploy.project.checkout_dir, after_checkout),
            shell=True)
