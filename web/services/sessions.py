#!/usr/local/bin/python
# -*- coding:utf-8 -*-
from web import db
from web.models.sessions import Sessions
from .base import Base
from web.utils.log import Logger
logger = Logger("web.services.sessions")
__author__ = 'Rocky Peng'


class SessionsService(Base):
    __model__ = Sessions


sessions = SessionsService()
