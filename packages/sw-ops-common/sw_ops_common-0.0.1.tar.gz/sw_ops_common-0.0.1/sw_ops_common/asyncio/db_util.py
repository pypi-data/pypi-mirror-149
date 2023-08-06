#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   db_util.py
@Time    :   2022/04/27 14:01:23
@Author  :   xy.xu
@Version :   1.0
@Contact :   xy.xu@shunwang.com
@Desc    :   None
'''
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import traceback
import pymysql
import log
import aiomysql
from config import settings


class PooledDBSingleton:

    @staticmethod
    async def instance():
        if hasattr(PooledDBSingleton, '_instance'):
            return PooledDBSingleton._instance
        if not hasattr(PooledDBSingleton, '_instance'):

            dbconfig = dict(
                host=settings.DB_HOST, 
                port=int(settings.DB_PORT), 
                user=settings.DB_USERNAME, 
                password=settings.DB_PASSWORD, db=settings.DB_DBNAME, charset='utf8')
            PooledDBSingleton._instance = await aiomysql.create_pool(**dbconfig)

        return PooledDBSingleton._instance


async def do_select_fetchall(sql, args=None, as_dict=False):
    try:
        pool = await PooledDBSingleton.instance()
        cursor_class = aiomysql.DictCursor if as_dict else aiomysql.Cursor
        result = []
        async with pool.acquire() as conn:
            async with conn.cursor(cursor_class) as cursor:
                await cursor.execute(sql, args)
                rows = await cursor.fetchall()
                for row in rows:
                    result.append(row)
                return result
                    
    except ConnectionError and pymysql.err.OperationalError as ce:
        log.error(f"mysql 链接 异常：{traceback.format_exc()}")
    except:
        log.error(f"mysql {sql.split(' ')[0]} 异常：{traceback.format_exc()}")


async def do_select_one(sql, args=None, as_dict=False):
    try:
        pool = await PooledDBSingleton.instance()
        cursor_class = aiomysql.DictCursor if as_dict else aiomysql.Cursor
        result = None
        async with pool.acquire() as conn:
            async with conn.cursor(cursor_class) as cursor:
                await cursor.execute(sql, args)
                row = await cursor.fetchone()
                if row is not None and len(row) > 0:
                    result = row[0]
                return result
                    
    except ConnectionError and pymysql.err.OperationalError as ce:
        log.error(f"mysql 链接 异常：{traceback.format_exc()}")
    except:
        log.error(f"mysql {sql.split(' ')[0]} 异常：{traceback.format_exc()}")


async def do_dml(sql, args=None):
    try:
        pool = await PooledDBSingleton.instance()
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(sql, args)
                    await conn.commit()
                except pymysql.err.IntegrityError as e:
                    await conn.rollback()
                    log.info(f"mysql insert 异常：{traceback.format_exc()}")
                    
    except ConnectionError and pymysql.err.OperationalError as ce:
        log.error(f"mysql 链接 异常：{traceback.format_exc()}")
    except:
        log.error(f"mysql {sql.split(' ')[0]} 异常：{traceback.format_exc()}")


async def do_batch_update(sqllist):

    result_list = []
    try:
        pool = await PooledDBSingleton.instance()

        async with pool.acquire() as conn:
            await conn.autocommit(False)
            async with conn.cursor() as cursor:
                try:
                    for sqlstr in sqllist:
                        rowcnt = await cursor.execute(sqlstr)
                        result_list.append(rowcnt)
                    await conn.commit()
                except pymysql.err.IntegrityError as e:
                    await conn.rollback()
                    log.info(f"mysql insert 异常：{traceback.format_exc()}")
                    
    except ConnectionError and pymysql.err.OperationalError as ce:
        log.error(f"mysql 链接 异常：{traceback.format_exc()}")
    except:
        log.error(f"mysql {sql.split(' ')[0]} 异常：{traceback.format_exc()}")

    return result_list


if __name__ == '__main__':
    import asyncio

    async def test():
        res = await do_select_fetchall('select * from deploy_order limit 1')
        print(res)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
