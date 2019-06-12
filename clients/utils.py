# -*- coding: utf-8 -*-
import configparser
import logging

import os

config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'local.ini')


def get_config():
    if not os.path.exists(CONFIG_PATH):
        logging.error('Please, provide config file')

    config.read(CONFIG_PATH)
    return config
