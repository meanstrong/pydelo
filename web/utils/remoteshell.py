#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

import time
import paramiko
from subprocess import CalledProcessError

from web.utils.log import Logger
logger = Logger("web.utils.remoteshell")


class RemoteShell(object):

    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.connect()

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.user, self.passwd, timeout=10)

    def exec_command(self, shell):
        logger.debug("remote shell: %s" % shell)
        # stdin, stdout, stderr = self.ssh.exec_command(shell)
        chan = self.ssh.get_transport().open_session()
        chan.exec_command(shell)
        buff_size = 1024
        stdout = ""
        stderr = ""
        while not chan.exit_status_ready():
            time.sleep(1)
            if chan.recv_ready():
                stdout += chan.recv(buff_size)
            if chan.recv_stderr_ready():
                stderr += chan.recv_stderr(buff_size)
        exit_status = chan.recv_exit_status()
        # Need to gobble up any remaining output after program terminates...
        while chan.recv_ready():
            stdout += chan.recv(buff_size)
        while chan.recv_stderr_ready():
            stderr += chan.recv_stderr(buff_size)
        logger.debug("rc: %d" % exit_status)
        logger.debug("stdout: %s" % stdout)
        logger.warn("stderr: %s" % stderr)
        return exit_status, stdout, stderr

    def check_call(self, shell):
        rc, stdout, stderr = self.exec_command(shell)
        if rc:
            raise CalledProcessError(rc, shell, stdout+"\n"+stderr)
        return rc

    def close(self):
        self.ssh.close()
