# -*- coding: utf-8 -*-
import configparser
import logging

import os

import telegram
from django.conf import settings

config = configparser.ConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CONFIG_PROFILE_PATH = os.environ.get('CONFIG_PROFILE_PATH', None)
if CONFIG_PROFILE_PATH is None:
    CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'prod.ini')
    logging.info("using {} config file".format(CONFIG_PATH))
else:
    logging.info("using {} config file".format(CONFIG_PROFILE_PATH))
    CONFIG_PATH = CONFIG_PROFILE_PATH

def get_config():
    if not os.path.exists(CONFIG_PATH):
        logging.error('Please, provide config file')

    config.read(CONFIG_PATH)
    return config


    # token that can be generated talking with @BotFather on telegram

