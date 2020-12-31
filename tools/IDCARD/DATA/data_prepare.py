#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-10-17 16:44
# @Author : dell

"""
解析行政区划代码.txt，并将数据保存到dbm数据库中。

行政区划代码.txt为国家统计局2017年3月10号版本，截止日期为2016年7月31日。
地址：http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201703/t20170310_1471429.html
该脚本为初始化城市信息并保存到数据库中，正式版本中请不要执行该脚本。

class:
    dataPrepare()
attr:
    city_info_list: list
method:
    get_city_info_from_file(self):
        从数据文件中读取新增区划信息，并保存到city_info_list中。
    create_db()：
        创建保存区划信息用的数据库并插入数据
"""

import dbm


class dataPrepare():
    """
    行政区划代码数据类。
    """
    def __init__(self):
        self.city_info_list = list()

    def get_city_info_from_file(self):
        """
        将行政区划代码从file中读取，并储存到self.city_info中。
        """
        city_code_file = 'cityCode.txt'
        with open(city_code_file) as city_code_fd:
            for line in city_code_fd:
                line = line.strip()
                if len(line):
                    [city_code, city_name] = line.split()
                    self.city_info_list.append((city_code, city_name))

    def create_db(self):
        """
        创建city_code表，并插入数据。
        :return:
        """
        city_info = dbm.open('city_database', 'c')
        for city_code, city_name in self.city_info_list:
            city_info[city_code] = city_name

if __name__ == '__main__':
    data_prepare = dataPrepare()
    data_prepare.get_city_info_from_file()
    data_prepare.create_db()

