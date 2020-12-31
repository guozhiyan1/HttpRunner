#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-11-07 15:28
# @Author : dell

import pytest
from assertpy import assert_that
from tools.IDCARD import IDCardProvide

class TestCreateIDNnmAllElements():

    def setup(self):
        self.idcard = IDCardProvide()

    def test_01_CreateIDNumAllElements_None(self):
        # 所有参数均为None
        with pytest.raises(TypeError) as ex_info:
            self.idcard.create_idnum_all_elements(None, None,None, None)
            assert_that(ex_info).is_equal_to('city_code, birthday, gender参数需要为list.')

    def test_02_CreateIDNumAllElements_Typeerror(self):
        # 传入参数不为list
        with pytest.raises(TypeError) as ex_info:
            self.idcard.create_idnum_all_elements('330681', '19871107', '1')
            assert_that(ex_info).is_equal_to('city_code, birthday, gender参数需要为list.')
        # 传入的不为字符串列表
        with pytest.raises(TypeError) as ex_info:
            self.idcard.create_idnum_all_elements([330681], [19871107], ['1'])
            assert_that(ex_info).is_equal_to('传入的参数必须为字符串列表。')

    def test_03_CreateIDNumAllElements_ListLengthNotEqual(self):
        # 传入的city_code列表长度较小
        assert_that(self.idcard.create_idnum_all_elements(['330681'], ['19871107', '19871108'], ['1', '0', '1'], is_multi=5)).is_length(1)
        # 传入的city_code列表长度较长
        assert_that(self.idcard.create_idnum_all_elements(['330681', '330682', '330683'], ['19871107', '19871108'], ['1'])).is_length(3)

    def test_04_CreateIDNumAllElements_Mutil(self):
        # 三要素为空,默认is_mutil=1
        assert_that(self.idcard.create_idnum_all_elements()).is_length(1)
        # 三要素为空，以is_mutil为准
        assert_that(self.idcard.create_idnum_all_elements(is_multi=5)).is_length(5)
        # 传入的列表的长度与is_mutil不一致，以city_code列表长度为准
        assert_that(self.idcard.create_idnum_all_elements(['330681', '330682'], ['19871107', '19871108'], ['1', '0'], is_multi=1)).is_length(2)

    def test_05_CreateIDNumAllElements_Gender(self):
        # 传入的非字符类型的gender
        with pytest.raises(ValueError) as ex_info:
            self.idcard.create_idnum_all_elements(['330681'], ['19871107'], [0])
            assert_that(ex_info).is_equal_to("gender：'0'代表女性，'1'代表男性，请传入'0'或者'1'.")
        # 传入错误的gender
        with pytest.raises(ValueError) as ex_info:
            self.idcard.create_idnum_all_elements(['330681'], ['19871107'], ['2'])
            assert_that(ex_info).is_equal_to("gender：'0'代表女性，'1'代表男性，请传入'0'或者'1'.")

    def test_06_CreateIDNumAllElements_Normal(self):
        # 传入长度为1的列表
        assert_that(self.idcard.create_idnum_all_elements(['330681'], ['19871107'], ['1'])).is_length(1)
        # 传入长度为2的列表
        assert_that(self.idcard.create_idnum_all_elements(['330681', '330682'], ['19871107', '19871108'], ['1', '0'])).is_length(2)

