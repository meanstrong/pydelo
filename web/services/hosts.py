#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.log import Logger
from web.models.hosts import Hosts

from .base import Base

logger = Logger("host service")


class HostsService(Base):
    __model__ = Hosts


hosts = HostsService()
