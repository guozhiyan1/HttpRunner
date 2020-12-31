#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-11-07 14:29
# @Author : dell

import pytest
from assertpy import assert_that
from tools.IDCARD import IDCardProvide


class TestResolutionIDNum():

    def setup(self):
        self.idcard = IDCardProvide()

    def test_01_ResolutionIDNum_Normal(self):
        # 性别男
        assert_that(self.idcard.resolution_idnum('330681198711070034')).is_equal_to(('浙江省绍兴市诸暨市', '1987-11-07', '1'))
        # 性别女
        assert_that(self.idcard.resolution_idnum('330681198711079768')).is_equal_to(('浙江省绍兴市诸暨市', '1987-11-07', '0'))

if __name__ == '__main__':
    pytest.main()