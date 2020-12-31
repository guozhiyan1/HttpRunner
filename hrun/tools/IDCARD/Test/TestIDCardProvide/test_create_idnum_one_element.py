#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-11-10 9:25
# @Author : dell

import pytest
from assertpy import assert_that
from tools.IDCARD import IDCardProvide

class TestCreateIDNumOneElement():

    def setup(self):
        self.idcard = IDCardProvide()

    def test_01_CreateIDNumOneElement_None(self):
        # 所有参数均为None
        with pytest.raises(ValueError) as ex_info:
            self.idcard.create_idnum_one_element(None)
            assert_that(ex_info).is_equal_to('三要素不能为空')
    def test_02_CreateIDNumOneElement_Typeerror(self):
        # 传入非字符串
        with pytest.raises(TypeError) as ex_info:
            self.idcard.create_idnum_one_element(330681)
            assert_that(ex_info).is_equal_to('三要素需要为字符串类型')

    def test_03_CreateIDNumOneElement_Lenth(self):
        # 行政区划代码长度大于6
        with pytest.raises(ValueError) as ex_info:
            self.idcard.create_idnum_one_element('3306811')
            assert_that(ex_info).is_equal_to('三要素长度要求为：城市行政代码6位，出生日期8位，性别为‘0’或者‘1’')

        # 行政区划代码长度小于6
        with pytest.raises(ValueError) as ex_info:
            self.idcard.create_idnum_one_element('33068')
            assert_that(ex_info).is_equal_to('三要素长度要求为：城市行政代码6位，出生日期8位，性别为‘0’或者‘1’')


