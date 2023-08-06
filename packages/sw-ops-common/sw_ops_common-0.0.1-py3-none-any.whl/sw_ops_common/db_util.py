#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   db_util.py
@Time    :   2022/02/28 11:34:33
@Author  :   xy.xu
@Version :   1.0
@Contact :   xy.xu@shunwang.com
@Desc    :   None
'''
import threading
import pymysql
from dbutils.pooled_db import PooledDB
from sw_ops_common.config import settings
DEFAULT_MAX_CONNECTIONS = 5


class PooledDBSingleton(object):
    """
        Implement a single-ton PooledDB, , that is thread-safe connection pool
        Refer to: http://www.webwareforpython.org/DBUtils/Docs/UsersGuide.html#persistentdb
    """
    _mutex = threading.Lock()
    _max_connection = DEFAULT_MAX_CONNECTIONS

    @staticmethod
    def instance():
        if hasattr(PooledDBSingleton, '_instance'):
            return PooledDBSingleton._instance
        PooledDBSingleton._mutex.acquire()
        try:
            if not hasattr(PooledDBSingleton, '_instance'):
                dbconfig = dict(host=settings.DB_HOST, port=int(settings.DB_PORT), user=settings.DB_USERNAME, passwd=settings.DB_PASSWORD, db=settings.DB_DBNAME, charset='utf8')
                PooledDBSingleton._instance = PooledDB(pymysql, maxconnections=PooledDBSingleton._max_connection, blocking=True, **dbconfig)
        finally:
            PooledDBSingleton._mutex.release()

        return PooledDBSingleton._instance

    @staticmethod
    def set_max_connections(value):
        if hasattr(PooledDBSingleton, '_instance'):
            raise Exception('max_connections should be set before PooledDB object is created.')
        PooledDBSingleton._max_connection = value


def do_select_fetchall(sqlstr, args=None, as_dict=False):
    """
    Remarks:
        Do a query and return a recordset.
        share_conn_thread describe whether the connection object is from PooledDB or PersistentDB
    """
    result = []
    conn = PooledDBSingleton.instance().connection()
    try:
        if as_dict:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
        else:
            cursor = conn.cursor()
        cursor.execute(sqlstr, args)
        rows = cursor.fetchall()
        for row in rows:
            result.append(row)

        cursor.close()
    finally:
        if conn:
            conn.close()

    return result


def do_select_fetchone(sqlstr, args=None):
    """
    Remarks:
        Do a query and return the first record's first column
        return None if no record is found
        share_conn_thread describe whether the connection object is from PooledDB or PersistentDB
    """
    result = None
    conn = PooledDBSingleton.instance().connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sqlstr, args)
        row = cursor.fetchone()
        if row is not None and len(row) > 0:
            result = row[0]
        cursor.close()
    finally:
        if conn:
            conn.close()

    return result


def do_dml(sqlstr, args=None):
    """
    Remarks:
        like do some update,delete,insert to db
        return affect row count
        share_conn_thread describe whether the connection object is from PooledDB or PersistentDB
    """
    conn = PooledDBSingleton.instance().connection()
    try:
        conn.autocommit = False
        cursor = conn.cursor()
        result = cursor.execute(sqlstr, args)
        conn.commit()
        cursor.close()
    finally:
        if conn:
            conn.close()

    return result


def do_insert(sqlstr, args=None):
    result = None
    conn = PooledDBSingleton.instance().connection()
    try:
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute(sqlstr, args)
        cursor.execute('SELECT @@IDENTITY AS id')
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
    finally:
        if conn:
            conn.close()

    return result[0][0]


def do_batch_update(sqllist):
    """
    Remarks:
        execute a batch of sqllist in a transation
        it raises NoUpdatedException if no record is updated for any sql.
    """
    result_list = []
    conn = PooledDBSingleton.instance().connection()
    try:
        conn.autocommit = False
        cursor = conn.cursor()
        for sqlstr in sqllist:
            rowcnt = cursor.execute(sqlstr)
            result_list.append(rowcnt)

        conn.commit()
        cursor.close()
    finally:
        if conn:
            conn.close()

    return result_list


def do_batch_content_records(sqlstr, args=None):
    result = None
    conn = PooledDBSingleton.instance().connection()
    try:
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute('SET @uids := null;')
        cursor.execute(sqlstr, args)
        cursor.execute('SELECT @uids;')
        row = cursor.fetchone()
        result = row[0]
        conn.commit()
        cursor.close()
    finally:
        if conn:
            conn.close()

    return result
