#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   load_config.py
@Time    :   2022/04/27 10:33:53
@Author  :   xy.xu
@Version :   1.0
@Contact :   xy.xu@shunwang.com
@Desc    :   None
'''

import os
import yaml
import copy


class ConfigUtil:

    def __init__(self):
        self.conf_path = self.get_conf_path()

    def get_conf_path(self):
        env = os.environ.get("RUN_ENV", "dev")
        if env == "prod":
            conf_path = os.environ.get('CONF_PATH')
        else:
            conf_path = os.path.join(os.getcwd(), "app.yaml")
        return conf_path

    def parser_conf(self):
        with open(self.conf_path, "r", encoding="UTF-8") as f:
            params = yaml.load(f, Loader=yaml.FullLoader)
        return params

    def get_app_conf(self):
        with open(self.conf_path, "r", encoding="UTF-8") as f:
            params = yaml.load(f, Loader=yaml.FullLoader)
        app_config = copy.deepcopy(params)
        for key, values in params.items():
            app_config.update(values)
        return app_config

    def get_conf_by_section(self, section):
        with open(self.conf_path, "r", encoding="UTF-8") as f:
            params = yaml.load(f, Loader=yaml.FullLoader)
        return params.get(section, {})
