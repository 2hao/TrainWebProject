#!/usr/bin/python
# _*_ coding: utf-8 _*_
# 数据库引擎对象


import threading
import logging


class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect

engine = None


class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transaction = 0

    def is_init(self):
        return self.connection is not None

    def init(self):
        self.connection = _LasyConnection()
        self.transaction = 0

    def clearup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DbCtx


class _LasyConnection(object):
    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            _connection = engine.connect()
            logging.info('[CONNECTION [OPEN] connection <%s>...]' % hex(id(_connection)))
            self.connection = _connection

        return self.connection.cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            logging.info('[CONNECTION] [CLOSE] connection <%s>...' % hex(id(_connection)))
            _connection.close()


class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx





