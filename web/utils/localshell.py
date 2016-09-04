#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from subprocess import Popen, PIPE, CalledProcessError

from web.utils.log import Logger
logger = Logger("web.utils.localshell")


class LocalShell(object):

    @staticmethod
    def check_output(*args, **kargs):
        cmd = kargs.get("args") or args[0]
        logger.debug("local shell: %s" % cmd)
        process = Popen(*args, stdout=PIPE, stderr=PIPE, **kargs)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        rc = process.poll()
        logger.debug("rc: %d" % rc)
        logger.debug("stdout: %s" % stdout)
        logger.warn("stderr: %s" % stderr)
        if rc:
            raise CalledProcessError(rc, cmd, stdout)
        return stdout

    @staticmethod
    def call(*args, **kargs):
        cmd = kargs.get("args") or args[0]
        logger.debug("local shell: %s" % cmd)
        process = Popen(*args, stdout=PIPE, stderr=PIPE, **kargs)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        rc = process.poll()
        logger.debug("rc: %d" % rc)
        logger.debug("stdout: %s" % stdout)
        logger.warn("stderr: %s" % stderr)
        return rc

    @staticmethod
    def check_call(*args, **kargs):
        cmd = kargs.get("args") or args[0]
        logger.debug("local shell: %s" % cmd)
        process = Popen(*args, stdout=PIPE, stderr=PIPE, **kargs)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        rc = process.poll()
        logger.debug("rc: %d" % rc)
        logger.debug("stdout: %s" % stdout)
        logger.warn("stderr: %s" % stderr)
        if rc:
            raise CalledProcessError(rc, cmd, stdout+"\n"+stderr)
        return rc
