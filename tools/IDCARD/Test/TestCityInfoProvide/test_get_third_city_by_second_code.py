#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-11-06 13:10
# @Author : dell

import pytest
from assertpy import assert_that
from tools.IDCARD import CiytInfoProvide


class TestGetThirdCityBySecondCode():

    def setup(self):
        self.city_info_test = CiytInfoProvide()

    def test_01_GetThirdCityBySecondCodecode_None(self):
        # 传入None
        with pytest.raises(TypeError):
            self.city_info_test.get_third_city_by_second_code(None)

    def test_02_GetThirdCityBySecondCode_Typeerror(self):
        # 传入数字
        with pytest.raises(TypeError):
            self.city_info_test.get_third_city_by_second_code(330681)

    def test_04_GetThirdCityBySecondCode_Length(self):
        # 超过6位
        with pytest.raises(TypeError):
            self.city_info_test.get_third_city_by_second_code('3306811')
        # 小于6位，传入0
        with pytest.raises(TypeError):
            self.city_info_test.get_third_city_by_second_code('0')

    def test_05_GetThirdCityBySecondCode_NotExists(self):
        # 不存在的数据
        with pytest.raises(ValueError):
            self.city_info_test.get_third_city_by_second_code('990100')

    def test_06_GetThirdCityBySecondCode_Normal(self):
        # 正常调用
        iexcept = {'330601':'市辖区', '330602':'越城区', '330603':'柯桥区', '330604':'上虞区', '330624':'新昌县', '330681':'诸暨市', '330683':'嵊州市'}
        assert_that(self.city_info_test.get_third_city_by_second_code('330600')).is_equal_to(iexcept)

if __name__ == '__main__':
    pytest.main('--tb=native')