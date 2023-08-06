#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   redis_util.py
@Time    :   2022/04/27 14:55:54
@Author  :   xy.xu
@Version :   1.0
@Contact :   xy.xu@shunwang.com
@Desc    :   None
'''
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import settings
from redis.asyncio.sentinel import Sentinel


class RedisSentinelHelper:
    
    def __init__(self) -> None:
        sentinel_conf = settings.REDIS_SENTINEL
        self.service_name = sentinel_conf.get('SERVICE_NAME', '')
        self.password = sentinel_conf.get('PASSWORD', '')
        self.db = sentinel_conf.get('DB', 1)
        self.sentinel = Sentinel(sentinel_conf.get('SENTINELS', []), socket_timeout=0.5)
    
    @property
    def master(self):
        return self.sentinel.master_for(self.service_name, password=self.password, db=self.db)

    @property
    def slave(self):
        return self.sentinel.slave_for(self.service_name, password=self.password, db=self.db)

    async def get_key(self, key):
        res = await self.slave.get(key)
        return res
    
    async def set_key(self, key, value, ex=None, nx=None):
        await self.master.set(key, value, ex, nx=nx)

    async def get_hash(self, key, sub_key):
        res = await self.slave.hget(key, sub_key)
        return res


    async def set_hash(self, key, sub_key, sub_value):
        """
        设置hash key值
        :param key:
        :param sub_key:
        :param sub_value:
        :return:
        """
        await self.master.hset(key, sub_key, sub_value)

    async def set_hash_batch(self, key, kwargs):
        return await self.master.hmset(key, kwargs)

    async def get_hash(self, key, sub_key):
        return await self.slave.hget(key, sub_key)

    async def get_hash_batch(self, key, *args):
        return await self.slave.hmget(key, args)

    async def delete_key(self, key):
        return await self.master.delete(key)

    async def delete_hash_key(self, key, *sub_keys):
        return await self.master.hdel(key, *sub_keys)


if __name__ == '__main__':
    import asyncio

    async def test():
        cli = RedisSentinelHelper()
        # res = await cli.get_hash('userNameIdMap', 'cj.chang')
        # res = await cli.get_key('userNameIdMap')
        # await cli.set_key('test', '1999')
        res = await cli.get_key('test')
        res1 = await cli.set_hash_batch('192.168.1.100', {'app_group_marks': 'aa'})
        print(res)
        print(res1)

    asyncio.run(test())
