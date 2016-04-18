#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from web import db
from web.utils.log import Logger
from web.models.sessions import Sessions

from .base import Base

logger = Logger("session service")


class SessionsService(Base):
    __model__ = Sessions


sessions = SessionsService()
