#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2017-10-25 9:33
# @Author : dell

"""
用于居民身份证校验位计算、完整身份证号码校验。
详细计算方法参考：https://zh.wikisource.org/wiki/GB_11643-1999_%E5%85%AC%E6%B0%91%E8%BA%AB%E4%BB%BD%E5%8F%B7%E7%A0%81

class:
    IDCardProvide()
attr:
    city_info_provide:
        CiytInfoProvid类实例，保存所有行政区划信息
method:
    create_idnum_all_elements(self, city_code=list(), birthday=list(), gender=list(), is_multi=1):
        使用行政区划代码、出生日期、性别三要素生成身份证号码，支持同时生成多个
    create_idnum_one_element(self, element, is_multi=1):
        使用行政区划代码、出生日期、性别三要素中的一个生成身份证号码，支持同时生成多个
    check_idnum(self, idnum)：
        校验身份证号的合法性
    resolution_idnum(self, idnum):
        解析身份证号，返回城市名称、出生日期、性别三要素
"""

import time
import datetime
import random
# jmeter使用时需要将from语句中的IDCARD去除，直接用city_info_provide
from tools.IDCARD.city_info_provide import CiytInfoProvide


class IDCardProvide():
    """
    身份证信息计算、校验实现类。
    """
    def __init__(self):
        self.city_info_provide = CiytInfoProvide()

    def __idcard_rule(self, cbi_num):
        """
        身份证号码计算规则实现。

        传入身份证前17位，计算后返回完整的18位身份证。

        @type cbi_num: str
        @rtype: str
        @param city_code: 行政区划代码 + 出生日期 + 顺序号组成的身份证前17位
        @return: 完整的18位身份证号
        """
        # 占位字符权重
        weight = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2,1]
        # 校验位换算规则
        check_conversion = {'0':'1','1':'0','2':'X','3':'9','4':'8','5':'7','6':'6','7':'5','8':'4','9':'3','10':'2'}
        isum = 0
        for index, num in enumerate(cbi_num):
            isum += weight[index] * int(num)
        id_num = cbi_num + check_conversion[str(isum%11)]

        return id_num

    def __get_city_code(self, number, city_code=None):
        """
        从城市列表中获取指定数目的行政区划代码。

        @type number: int
        @rtype:list[str]
        @param number: 需要获取的行政区划的数目
        @return:行政区划代码组成的列表
        """
        city_code_list = list()
        if city_code:
            for num in range(number):
                city_code_list.append(city_code)
        else:
            # jpython 无法使用choices，修改为random
            # city_code_list = random.choices(list(self.city_info_provide.all_city_info.keys()), k=number)
            all_city_code_list = list(self.city_info_provide.all_city_info.keys())
            length = len(all_city_code_list)
            city_code_list = list()
            for index in range(number):
                random_int = random.randint(0, length)
                city_code_list.append(all_city_code_list[random_int])

        return city_code_list

    def __get_birthday(self, number, birthday=None):
        """
        随机生成指定数目的出生日期。

        @type number: int
        @rtype: list[str]
        @param number: 需要生成的出生日期的数目
        @return: 出生日期组成的列表
        """
        birthday_list = list()
        if birthday:
            for num in range(number):
                birthday_list.append(birthday)
        else:
            taday = datetime.date.today()
            birthday_list = [(taday - datetime.timedelta(days=random.randint(0, 365*100))).strftime('%Y%m%d') for num in range(number)]

        return birthday_list

    def __get_gender(self, number, gender=None):
        """
        随即生成指定数目的性别标识。

        @type number: int
        @rtype: list[str]
        @param num: 需要生成的性别标识的数目
        @return: 0,1组成的列表
        """
        gender_list = list()
        if gender:
            for num in range(number):
                gender_list.append(gender)
        else:
            gender_list = [str(random.randint(0,1)) for num in range(number)]

        return gender_list

    def create_idnum_all_elements(self, city_code=list(), birthday=list(), gender=list(), is_multi=1):
        """
        使用行政区划代码、出生日期、性别三要素生成身份证号码。

        默认只生成一条身份证号码，传入is_multi参数可批量生成；生成多条时有一定几率出现相同的身份证号。
        PS:行政区划代码未做类型判断（部分城市无区县一级行政区，如台湾、香港等均未做排除）,故部分身份证
        号实际中不存在。
        关于city_code,birthday,gender参数：
        1、三者必须同时传入或者同时不传
        2、若三者均不传或者传入列表为空，则生成身份证的数量由is_multi参数控制,否则以city_code实际长度为准
        3、同时传入时，建议三者的列表长度一致
        4、同时传入时，若三者列表长度不一致，则以city_code实际长度为准，且除city_code外参数随机生成
        5、若传入的列表长度与is_mutil参数不符，则以列表长度为准
        6、若参数显式传入则不校验各个参数值的有效性，可能出现实际不存在、无法使用的身份证号码

        @type city_code: list
        @type birthday: list
        @type gender: list['0' | '1']
        @type is_multi: int
        @rtype: list[str]
        @param city_code: 6位行政区划代码
        @param birthday: 8位出生日期
        @param gender: 性别，0代表女性，1代表男性
        @param is_multi: 生成数量，默认为1
        @return: 身份证号码组成的列表
        """
        index_list = list()
        idnum_list = list()

        if city_code is None \
                or birthday is None \
                or gender is None \
                or not isinstance(city_code, list)\
                or not isinstance(birthday, list)\
                or not isinstance(gender, list):
            raise TypeError('city_code, birthday, gender参数需要为list.')
        # 若三者列表长度不同，则以city_code为准
        if len(city_code)+len(birthday) != len(birthday)+len(gender) and len(city_code) != 0:
            is_multi = len(city_code)
            city_code_list = city_code
            birthday_list = self.__get_birthday(is_multi)
            gender_list = self.__get_gender(is_multi)
        # 若三者列表长度均为0，则以is_mutil为准
        elif len(city_code) == 0:
            city_code_list = self.__get_city_code(is_multi)
            birthday_list = self.__get_birthday(is_multi)
            gender_list = self.__get_gender(is_multi)
        # 若三者列表长度相同且不为零，则以实际列表为准
        else:
            is_multi = len(city_code)
            city_code_list = city_code
            birthday_list = birthday
            gender_list = gender

        # 依据生成的gender列表生成顺序号
        for gender_flag in gender_list:
            if gender_flag not in ['0', '1']:
                raise ValueError("gender：'0'代表女性，'1'代表男性，请传入'0'或者'1'.")
            while True:
                index_temp = random.sample('0123456789',3)
                if int(index_temp[2])%2 == int(gender_flag):
                    index_list.append(''.join(index_temp))
                    break
        # 生成身份证号
        try:
            for num in range(is_multi):
                idnum = city_code_list[num] + birthday_list[num] + index_list[num]
                idnum_list.append(self.__idcard_rule(idnum))
        except TypeError:
            raise TypeError('传入的参数必须为字符串列表。')

        return idnum_list

    def create_idnum_one_element(self, element, is_multi=1):
        """
        使用城市、出生日期、性别中的一个要素生成身份证号码。

        要素通过通过传入参数的长度判断，行政区划代码为6位，出生日期为8位，性别为1位。

        @type element: str | int
        @type is_multi: int
        @rtype: list[str]
        @param element: 行政区划代码、出生日期、性别三个要素中的一个
        @param is_multi: 生成数量，默认为1
        @return: 身份证号码组成的列表
        """
        if element is None:
            raise ValueError('三要素不能为空')
        elif not isinstance(element, str):
            raise TypeError('三要素需要为字符串形式')

        element_len = len(str(element))
        if element_len == 6:
            city_code = self.__get_city_code(is_multi, element)
            birthday = self.__get_birthday(is_multi)
            gender = self.__get_gender(is_multi)
        elif element_len == 8:
            city_code = self.__get_city_code(is_multi)
            birthday = self.__get_birthday(is_multi, element)
            gender = self.__get_gender(is_multi)
        elif element in ['0','1']:
            city_code = self.__get_city_code(is_multi)
            birthday = self.__get_birthday(is_multi)
            gender = self.__get_gender(is_multi, element)
        else:
            raise ValueError('三要素长度要求为：城市行政代码6位，出生日期8位，性别为‘0’或者‘1’')

        idnum_list = self.create_idnum_all_elements(city_code, birthday, gender)

        return idnum_list

    def check_idnum(self, idnum):
        """
        校验身份证号是否符合规范。

        @type idnum: str
        @rtype: bool
        @param idnum: 18位身份证号
        @return: 合规返回True,否则返回False
        """
        if not isinstance(idnum, (str)) or len(idnum) != 18:
            raise TypeError('请传入18位身份证号,需要为字符串形式')
        if idnum[0:6] not in self.city_info_provide.all_city_info:
            raise ValueError('行政区划代码不存在')
        try:
            time.strptime(idnum[6:14], '%Y%m%d')
        except Exception:
            raise ValueError('出生日期不符合规范')
        if idnum == self.__idcard_rule(idnum[0:-1]):
            return True
        else:
            return False

    def resolution_idnum(self, idnum):
        """
        解析身份证号，输出城市、生日、性别。

        @type idnum: str | int
        @rtype:
        @param idnum:
        @return:
        """
        try:
            self.check_idnum(idnum)
        except Exception:
            raise Exception

        city_code = idnum[0:6]
        birthday = idnum[6:14]
        index = idnum[14:17]
        city_name = self.city_info_provide.get_city_by_code(city_code)
        birthday = time.strftime('%Y-%m-%d', time.strptime(birthday, '%Y%m%d'))
        if int(index)%2 == 0:
            gender = '0' # 0表示女性
        else:
            gender = '1' # 1表示男性

        return (city_name, birthday, gender)

if __name__ == '__main__':
    test = IDCardProvide()
    # '0'代表女性，'1'代表男性
    # 随机生成一个身份证号码
    # num_list = test.create_idnum_all_elements()

    # 随机生成多个身份证号码
    # num_list = test.create_idnum_all_elements(is_multi=10)

    # 传入行政区划代码、出生年月日、性别三要素生成身份证号码
    # num_list = test.create_idnum_all_elements(['330681'], ['19911104'],['1'])

    # 传入多个三要素，三要素需要全部传入且数目相同
    num_list = test.create_idnum_all_elements(['330681', '330683'], ['19911104', '19911105'], ['1', '0'])

    # 使用单一要素随机生成一个身份证号码（可传入6位行政区划代码、8位出生日期、1位性别标志）
    # num_list = test.create_idnum_one_element('1')

    # 使用单一要素随机生成多个身份证号码
    # num_list = test.create_idnum_one_element('1', is_multi=10)

    # 校验身份证号码是否合法
    flag = test.check_idnum('511423198711020037')

    # 解析身份证号码
    (city_name, birthday, gender) = test.resolution_idnum('511423198711020037')
    print(city_name, birthday, gender)


