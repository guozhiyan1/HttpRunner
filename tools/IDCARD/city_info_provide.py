#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-10-23 13:44
# @Author : dell

"""
city_info操作类。

将城市信息从dbm中读取到内存中，并做初步处理。

class:
    CityInfoProvide()
attr:
    first_city:
        {省级行政代码：名称},省一级行政区划的字典
    second_city：
        {地市级行政代码：名称}，地市一级行政区划的字典
    third_city：
        {区县级行政代码：名称}，区县一级行政区划的字典
    all_city_info：
        所有行政区划的列表
method:
    get_city_by_code(self, city_code):
        通过城市行政代码查询城市信息
    get_second_city_by_first_code(self, first_city_code):
        查询省级行政区下的所有地市级行政区
    get_third_city_by_second_code(self, second_city_code):
        查询地市级行政区下的所有区县级行政区
"""

import dbm
import os
from tools.IDCARD.city_info import CityInfo


class CiytInfoProvide():
    """
    city_info信息类。
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(CiytInfoProvide, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self):
        self.first_city = dict() # @type: dict[省级行政代码：名称]
        self.second_city = dict() # @type: dict[地市级行政代码：名称]
        self.third_city = dict() # @type: dict[区县级行政代码：名称]
        self.all_city_info = dict() # @type: dict[CityInfo]
        self.__load_city_info()

    def __load_city_info(self):
        """
        从db文件中将城市信息加载到内存中.
        """
        # 不止为何在pytest测试时dbm路径必须为绝对路径
        db_file_path = os.path.join(os.path.dirname(__file__), 'DATA/city_database')
        city_info = dbm.open(db_file_path)
        for city_code, city_name in city_info.items():
            city_code = city_code.decode('utf-8')
            city_name = city_name.decode('utf-8')
            if city_code.endswith('0000'): # '0000'代表省级行政区
                self.first_city[city_code] = city_name
            elif city_code.endswith('00'): # '00'代表地市级行政区
                self.second_city[city_code] = city_name
            else:
                self.third_city[city_code] = city_name
            self.all_city_info[city_code] = CityInfo(city_code, city_name)

    def get_city_by_code(self, city_code):
        """
        通过城市行政代码查询城市信息。

        @type city_code: str
        @rtype: str
        @param city_code: 城市行政区划代码
        @return: 省市区
        """
        if not isinstance(city_code, str) or len(city_code) != 6:
            raise TypeError('请输入正确的6位行政区划代码:{}'.format(city_code))
        elif city_code not in self.all_city_info:
            raise ValueError('行政区划代码不存在：{}'.format(city_code))
        first_city = self.first_city.get(city_code[0:2] + '0000') # 前两位+'0000'代表省级行政区
        second_city = self.second_city.get(city_code[0:4] + '00', '') # 前两位+'00'代表地市级行政区
        third_city = self.third_city.get(city_code, '')
        complate_city = (first_city + second_city + third_city).strip()

        return complate_city

    def get_second_city_by_first_code(self, first_city_code):
        """
        依据省一级行政区划代码，查询出所有地市一级的列表。

        @type first_city_code: str
        @rtype: dict[city_code:city_name]
        @param first_city_code: 省一级6位行政区划代码
        @return: {city_code:city_name}城市行政区划代码,城市名称的字典。
        """
        if not isinstance(first_city_code, str) or len(first_city_code) != 6:
            raise TypeError('请输入正确的6位行政区划代码:{}'.format(first_city_code))
        elif first_city_code not in self.all_city_info:
            raise ValueError('行政区划代码不存在：{}'.format(first_city_code))
        second_city = dict()
        for city_code, city_name in self.second_city.items():
            if city_code.startswith(first_city_code[0:2]):
                second_city[city_code] = city_name

        return second_city

    def get_third_city_by_second_code(self, second_city_code):
        """
        依据地市一级行政区划代码，查询出所有县市一级的列表。

        @type: str
        @rtype: dict[city_code:city_name]
        @param second_city_code: 地市一级6位行政区划代码
        @return: {city_code:city_name}城市行政区划代码,城市名称的字典。
        """
        if not isinstance(second_city_code, str) or len(second_city_code) != 6:
            raise TypeError('请输入正确的6位行政区划代码:{}'.format(second_city_code))
        elif second_city_code not in self.all_city_info:
            raise ValueError('行政区划代码不存在：{}'.format(second_city_code))
        third_city = dict()
        for city_code, city_name in self.third_city.items():
            if city_code.startswith(second_city_code[0:4]) and not city_code.endswith('00'):
                third_city[city_code] = city_name

        return third_city

if __name__ == '__main__':
    test = CiytInfoProvide()
    res = test.get_third_city_by_second_code('330600')



