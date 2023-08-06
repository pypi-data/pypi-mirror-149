#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2022/04/27 10:33:13
@Author  :   xy.xu
@Version :   1.0
@Contact :   xy.xu@shunwang.com
@Desc    :   None
'''

from config.load_config import ConfigUtil


class Settings:

    def __init__(self):
        pass

    def _setup(self):
        self._wrapped = ConfigUtil().parser_conf()
    
    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__.get(name, None)
        else:
            if self._wrapped is None:
                self._setup()
            return self._wrapped.get(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            if self._wrapped is None:
                self._setup()
            self._wrapped[name] = value
        return

settings = Settings()