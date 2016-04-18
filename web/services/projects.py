#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.log import Logger
from web.models.projects import Projects
from web.utils.git import Git

from .base import Base

logger = Logger("project service")


class ProjectsService(Base):
    __model__ = Projects

    def git_clone(self, project_id):
        project = self.get(project_id)
        git = Git(project.checkout_dir, project.repo_url)
        git.clone()

    def git_branch(self, project_id):
        project = self.get(project_id)
        git = Git(project.checkout_dir, project.repo_url)
        return git.branch()

    def git_log(self, project_id, branch):
        project = self.get(project_id)
        git = Git(project.checkout_dir, project.repo_url)
        return git.log(branch)

projects = ProjectsService()
