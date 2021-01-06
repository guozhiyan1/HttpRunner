#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-11-06 14:13
# @Author : dell

import pytest
from assertpy import assert_that
from tools.IDCARD import IDCardProvide


class TestCheckIDNum():

    def setup(self):
        self.idcard = IDCardProvide()

    def test_01_CheckIDNum_None(self):
        # None
        with pytest.raises(TypeError):
            self.idcard.check_idnum(None)

    def test_02_CheckIDNum_Typeerror(self):
        # Typeerror
        with pytest.raises(TypeError):
            self.idcard.check_idnum(330681198711070034)

    def test_03_CheckIDNum_Length(self):
        # 超过18位
        with pytest.raises(TypeError):
            self.idcard.check_idnum('3306811987110700341')

        # 小于十八位
        with pytest.raises(TypeError):
            self.idcard.check_idnum('0')

    def test_04_CheckIDNum_ErrorIDNum(self):
        # 行政区划代码错误
        with pytest.raises(ValueError) as ex_info:
            self.idcard.check_idnum('330688198711070034')
            assert_that(ex_info).is_equal_to('行政区划代码不存在')
        # 出生日期错误
        with pytest.raises(ValueError) as ex_info:
            self.idcard.check_idnum('330681198713070034')
            assert_that(ex_info).is_equal_to('出生日期不符合规范')
        # 校验位错误
        assert_that(self.idcard.check_idnum('330681198711070035')).is_false()

    def test_05_CheckIDNum_Normal(self):
        # 正常调用
        assert_that(self.idcard.check_idnum('330681198711070034'))

if __name__ == '__main__':
    pytest.main('--tb=native')