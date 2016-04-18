#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web.utils.localshell import LocalShell
from web.utils.log import Logger

logger = Logger("GIT")


class Git(object):

    def __init__(self, dest, url):
        self.dest = dest
        self.url = url

    def branch(self):
        shell = "cd {0} && git fetch -q -a && git branch -r".format(self.dest)
        stdout = LocalShell.check_output(shell, shell=True)
        stdout = stdout.strip().split("\n")
        stdout = [s.strip(" ").split("/", 1)[1] for s in stdout if "->" not in s]
        return stdout

    def log(self, branch):
        shell = ("cd {0} && git checkout -q {1} && git fetch -q --all && "
                 "git log -20 --pretty=\"%h  %an  %s\"").format(self.dest, branch)
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
            shell = ("cd {0} && git clean -xdfq && git reset -q --hard && git checkout -q master && git remote update && git remote prune origin && git pull -q --all && git branch | grep -v \\* | xargs git branch -D").format(self.dest)
            rc = LocalShell.call(shell, shell=True)
            # branch name required
            if rc == 123:
                return
        if rc != 0:
            raise Error(12000)

    def checkout(self, branch, version):
        logger.debug("checkout:")
        LocalShell.check_call(
            "cd {0} && git checkout -B {1} -t origin/{1} && git pull -q origin {1} && git reset --hard {2}".format(
                self.dest, branch, version),
            shell=True)
