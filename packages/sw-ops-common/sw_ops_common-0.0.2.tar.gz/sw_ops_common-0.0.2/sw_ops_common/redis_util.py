#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   redis_util.py
@Time    :   2022/05/06 10:17:37
@Author  :   xy.xu
@Version :   1.0
@Contact :   xy.xu@shunwang.com
@Desc    :   None
'''

import threading
from redis.sentinel import Sentinel
from sw_ops_common.config import settings


class RedisSentinelHelper:

    _instance = None
    _mutex = threading.Lock()

    @staticmethod
    def instance():
        if hasattr(RedisSentinelHelper, '_instance'):
            return RedisSentinelHelper._instance
        RedisSentinelHelper._mutex.acquire()
        try:
            if not hasattr(RedisSentinelHelper, '_instance'):
                RedisSentinelHelper._instance = RedisSentinelHelper()
        finally:
            RedisSentinelHelper._mutex.release()

        return RedisSentinelHelper._instance

    def __init__(self):
        sentinel_conf = settings.REDIS_SENTINEL
        self.service_name = sentinel_conf.get('SERVICE_NAME', '')
        self.password = sentinel_conf.get('PASSWORD', '')
        self.db = sentinel_conf.get('DB', 1)
        self.sentinel = Sentinel(sentinel_conf['SENTINELS'], socket_timeout=0.5)  

    def get_master(self):
        return self.sentinel.master_for(
            service_name=self.service_name,
            socket_timeout=self.socket_timeout,
            password=self.password,
            db=self.db
        )

    def get_slave(self):
        return self.sentinel.slave_for(
            service_name=self.service_name,
            socket_timeout=self.socket_timeout,
            password=self.password,
            db=self.db
        )

    def get_pipeline(self):
        master = self.get_master()
        return master.pipeline

    def set_key(self, key, value, ex=None, nx=None):
        master = self.get_master()
        return master.set(key, value, ex, nx=nx)

    def get_key(self, key):
        slave = self.get_slave()
        return slave.get(key)

    def expire_key(self, key, seconds):
        master = self.get_master()
        return master.expire(key, seconds)

    def set_hash(self, key, sub_key, sub_value):
        """
        设置hash key值
        :param key:
        :param sub_key:
        :param sub_value:
        :return:
        """
        master = self.get_master()
        return master.hset(key, sub_key, sub_value)

    def set_hash_batch(self, key, kwargs):
        master = self.get_master()
        return master.hmset(key, kwargs)

    def get_hash(self, key, sub_key):
        slave = self.get_slave()
        return slave.hget(key, sub_key)

    def get_hash_batch(self, key, *args):
        slave = self.get_slave()
        return slave.hmget(key, args)

    def delete_key(self, key):
        master = self.get_master()
        return master.delete(key)

    def delete_hash_key(self, key, *sub_keys):
        master = self.get_master()
        return master.hdel(key, *sub_keys)
