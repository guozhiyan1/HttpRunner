#! /usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os

parse = configparser.ConfigParser()

root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0]
config_path = os.path.join(root_path, "config.conf")


def init():
    parse.read(config_path, encoding="utf-8")


def get_conf(group, key):
    init()
    return parse.get(group, key)


# class LoadConfig(object):
#     cf = ''
#     file_path = "config.conf"
#
#     def __init__(self):
#         try:
#             f = open(self.file_path, 'r', encoding="utf-8")
#         except IOError as e:
#             print("\"%s\" Config file not found." % self.file_path)
#             sys.exit(1)
#         f.close()
#
#         self.cf = ConfigParser()
#         self.cf.read(self.file_path, encoding="utf-8")
#
#     def get_section_value(self, section, key):
#         return self.get_format(self.cf.get(section, key))
#
#     def get_section_options(self, section):
#         return self.cf.options(section)
#
#     def get_section_items(self, section):
#         return self.cf.items(section)
#
#     @staticmethod
#     def get_format(string):
#         return string.strip("'").strip('"').replace(" ", "")
#
