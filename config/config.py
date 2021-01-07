#! /usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os

parse = configparser.ConfigParser()

root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0]
config_path = os.path.join(root_path, "config.conf")


def init():
    parse.read(config_path)


def get_conf(group, key):
    init()
    return parse.get(group, key)
