#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-11-06 13:09
# @Author : dell

import pytest
from assertpy import assert_that
from tools.IDCARD import CiytInfoProvide


class TestGetSecondCityByFirstCode():

    def setup(self):
        self.city_info_test = CiytInfoProvide()

    def test_01_GetSecondCityByFirstCode_None(self):
        # 传入None
        with pytest.raises(TypeError):
            self.city_info_test.get_second_city_by_first_code(None)

    def test_02_GetSecondCityByFirstCode_Typeerror(self):
        # 传入数字
        with pytest.raises(TypeError):
            self.city_info_test.get_second_city_by_first_code(330681)

    def test_04_GetSecondCityByFirstCode_Length(self):
        # 超过6位
        with pytest.raises(TypeError):
            self.city_info_test.get_second_city_by_first_code('3306811')
        # 小于6位
        with pytest.raises(TypeError):
            self.city_info_test.get_second_city_by_first_code('0')

    def test_05_GetSecondCityByFirstCode_NotExists(self):
        # 不存在的数据
        with pytest.raises(ValueError):
            self.city_info_test.get_second_city_by_first_code('990000')

    def test_06_GetSecondCityByFirstCode_Normal(self):
        # 正常调用
        iexcept = {'330100':'杭州市', '330200':'宁波市', '330300':'温州市', '330400':'嘉兴市', '330500':'湖州市','330600':'绍兴市', '330700':'金华市', '330800':'衢州市', '330900':'舟山市', '331000':'台州市', '331100':'丽水市'}
        assert_that(self.city_info_test.get_second_city_by_first_code('330000')).is_equal_to(iexcept)

if __name__ == '__main__':
    pytest.main('--tb=native')