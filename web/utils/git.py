#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web.utils.localshell import LocalShell
from web.utils.log import Logger
from web.utils.error import Error

logger = Logger("GIT")


class Git(object):

    def __init__(self, dest, url):
        self.dest = dest
        self.url = url

    def local_branch(self):
        shell = "cd {0} && git fetch -q -a && git branch".format(self.dest)
        stdout = LocalShell.check_output(shell, shell=True)
        stdout = stdout.strip().split("\n")
        stdout = [s.strip("* ") for s in stdout]
        return stdout

    def remote_branch(self):
        shell = "cd {0} && git fetch -q -a && git branch -r".format(self.dest)
        stdout = LocalShell.check_output(shell, shell=True)
        stdout = stdout.strip().split("\n")
        stdout = [s.strip(" ").split("/", 1)[1] for s in stdout if "->" not in s]
        return stdout

    def tag(self):
        shell = "cd {0} && git fetch -q -a && git tag".format(self.dest)
        stdout = LocalShell.check_output(shell, shell=True)
        if stdout:
            return stdout.strip().split("\n")
        else:
            return []

    def log(self):
        shell = ("cd {0} && git log -20 --pretty=\"%h  %an  %s\"").format(self.dest)
        stdout = LocalShell.check_output(shell, shell=True)
        stdout = stdout.strip().split("\n")
        stdout = [s.split("  ", 2) for s in stdout]
        return [{"abbreviated_commit": s[0],
                 "author_name": s[1],
                 "subject": s[2]}
                for s in stdout]

    def clone(self):
        logger.debug("clone repo:")
        shell = ("mkdir -p {0} && cd {0} && git clone -q {1} .").format(self.dest, self.url)
        rc = LocalShell.call(shell, shell=True)
        # destination path '.' already exists and is not an empty directory.
        if rc == 128:
            shell = ("cd {0} && git clean -xdfq && git reset -q --hard && git remote update && git checkout -q master && git remote prune origin && git pull -q --all && git branch | grep -v \\* | xargs git branch -D").format(self.dest)
            rc = LocalShell.call(shell, shell=True)
            # branch name required
            if rc == 123:
                return
        if rc != 0:
            raise Error(12000)

    def checkout(self, branch=None, version=None, tag=None):
        logger.debug("checkout:")
        if branch is None or version is None:
            LocalShell.check_call(
                "cd {0} && git checkout {1}".format(self.dest, tag),
                shell=True)
        else:
            if branch in self.local_branch():
                LocalShell.check_call(
                    "cd {0} && git checkout {1} && git pull -q origin {1} && git reset --hard {2}".format(
                        self.dest, branch, version),
                        shell=True)
            else:
                LocalShell.check_call(
                    "cd {0} && git checkout -b {1} -t origin/{1} && git pull -q origin {1} && git reset --hard {2}".format(
                        self.dest, branch, version),
                        shell=True)
