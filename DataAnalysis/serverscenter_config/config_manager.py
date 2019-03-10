# -*- coding: utf-8 -*-
import json
import os

from custom_class import SingletonInstance


class ConfigManager(SingletonInstance):
    def __init__(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/secret_data.json") as data_file:
            self._config = json.load(data_file)

    def get_db_host(self):
        return self._config['MARIA_HOST']

    def get_db_port(self):
        return self._config['MARIA_PORT']

    def get_db_name(self):
        return self._config['MARIA_DB']

    def get_db_id(self):
        return self._config['MARIA_ID']

    def get_db_pw(self):
        return self._config['MARIA_PW']

    def get_dongyang_id(self):
        return self._config['DONGYANG_ID']

    def get_dongyang_pw(self):
        return self._config['DONGYANG_PW']
