#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-11-03 15:14
# @Author : dell

import pytest
from assertpy import assert_that
from tools.IDCARD import CiytInfoProvide


class TestGetCityByCode():

    def setup(self):
        self.city_info_test = CiytInfoProvide()

    def test_01_GetCityByCode_None(self):
        # 传入None
        with pytest.raises(TypeError):
            self.city_info_test.get_city_by_code(None)

    def test_02_GetCityByCode_Typeerror(self):
        # 传入数字
        with pytest.raises(TypeError):
            self.city_info_test.get_city_by_code(330681)

    def test_04_GetCityByCode_Length(self):
        # 超过6位
        with pytest.raises(TypeError):
            self.city_info_test.get_city_by_code('3306811')
        # 小于6位
        with pytest.raises(TypeError):
            self.city_info_test.get_city_by_code('0')

    def test_05_GetCityByCode_NotExists(self):
        # 不存在的数据
        with pytest.raises(ValueError):
            self.city_info_test.get_city_by_code('123456')

    def test_06_GetCityByCode_Normal(self):
        # 正常调用
        iexcept = '浙江省绍兴市诸暨市'
        assert_that(self.city_info_test.get_city_by_code('330681')).is_equal_to(iexcept)

    def test_07_GetCityByCode_Province(self):
        # 省级行政区
        iexcept = '浙江省'
        assert_that(self.city_info_test.get_city_by_code('330000')).is_equal_to(iexcept)

    def test_08_GetCityByCode_Prefecture(self):
        # 地级市
        iexcept = '浙江省绍兴市'
        assert_that(self.city_info_test.get_city_by_code('330600')).is_equal_to(iexcept)

if __name__ == '__main__':
    pytest.main('--tb=native')