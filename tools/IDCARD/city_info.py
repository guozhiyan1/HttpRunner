#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-10-18 14:16
# @Author : dell

"""
城市信息类

class:
    CityInfo()

attr:
    city_code:城市行政代码
    city_name:城市名称
    city_type:城市类型（省、市、区）
    up_level_city:上一级城市的信息，默认为空
    next_level_city:下一级城市的信息，默认为空

method:
    set_up_level_city(self, up_city_info):
        设置城市的上一级城市
    set_next_level_city(self, next_city_info):
        设置城市的下一级城市
"""


class CityInfo():
    """
    城市信息类
    """

    def __init__(self, city_code, city_name):
        self.city_code = city_code
        self.city_name = city_name
        self.up_city = dict()
        self.next_city = dict()

    def set_up_level_city(self, up_city):
        """
        设置城市的上一级城市

        @type up_city: str
        @param up_city: 上一级城市的城市信息
        """
        self.up_city = up_city

    def set_next_level_city(self, next_city):
        """
        设置城市的下一级城市

        @type next_city: str
        @param next_city: 下一级城市的城市信息
        """
        self.next_city = next_city
