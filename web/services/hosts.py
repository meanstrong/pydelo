#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from web import db
from web.models.hosts import Hosts
from .base import Base
from web.utils.log import Logger
logger = Logger("host service")
__author__ = 'Rocky Peng'


class HostsService(Base):
    __model__ = Hosts

hosts = HostsService()
