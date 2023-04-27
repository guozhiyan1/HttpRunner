import os
import random
import string
import time
import datetime

import calendar
from gmc_http_tools import logger

from tools import gmc_mysql, generate_date, generate_run_sql, genenate_chinese_name
import faker
from data import basic_dict

BASE_URL = "http://127.0.0.1:5000"
fake = faker.Faker(locale='zh_CN')
sql_data_dicts = basic_dict.sql_data_dicts


def sum_two(m, n):
    return m + n


def sum_subtraction(m, n):
    return m - n


def sleep_time(i):
    for i in range(i):
        time.sleep(1)
        print(f"前置方法暂停{i}秒")


def get_random_string(str_len):
    random_char_list = []
    for _ in range(str_len):
        random_char = random.choice(string.ascii_letters + string.digits)
        random_char_list.append(random_char)

    random_string = ''.join(random_char_list)
    return random_string


def setup_hook_add_kwargs(request):
    request["key"] = "value"


def setup_hook_remove_kwargs(request):
    request.pop("key")


def alter_response(response):
    response.status_code = 500
    response.headers["Content-Type"] = "html/text"
    response.json["headers"]["Host"] = "127.0.0.1:8888"
    response.new_attribute = "new_attribute_value"
    response.new_attribute_dict = {
        "key": 123
    }


def get_token(token):
    try:
        token = token['token_type'] + " " + token["access_token"]
    except Exception as e:
        logger.log_info("token  获取失败  %s %s" % (token, e))
    return token


def get_date(**kwargs):
    """
    "%Y-%m-%d"
    "%Y-%m-%d %H:%M:%S"
    "%Y-%m-%dT%H:%M:%S.000Z"
    add_date=None
    delete_date=None
    """
    return generate_date.getdate(**kwargs)


def stamp():
    return time.time()


def get_millisecond_stamp():
    t = time.time()
    return int(round(t*1000))


def get_outpatient_no():
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    number = ''.join(random.sample('0123456789', 3))
    return date+"000"+number


def get_number(n):
    new_number = ''.join(random.sample('0123456789', n))
    return new_number


def get_card_number():
    return fake.ssn(min_age=18, max_age=90)


def gmc_run_mysql(*args, **kwargs):
    s = generate_run_sql.RunSql(sql_data_dicts, *args, **kwargs)
    return s.get_sql_result()

def get_sql_result(*args, **kwargs):
    s = generate_run_sql.RunSql(sql_data_dicts, *args, **kwargs)
    return s.validation_sql()

def reload_dict():
    global sql_data_dicts
    sql_data_dicts = basic_dict.get_patient_data()


def get_result_dicts(key):
    return sql_data_dicts[key]


def get_list_dict_value(value_list, key, value, result):
    """
    取随机列表当中，key=value对应的字典中 想要的字段的值。
    如body = [{1:2,3:4},{5:6}]
    get_list_dict_value(如body, 1, 2, 3)
    返回值=4
    """
    print(value_list, '\n',  key, value, result)
    for i in value_list:
        print(i[key])
        if i[key] == value:
            print(i[result])
            return str(i[result])

#[{1:2,3:4}]获取值使用；/app-schedule-manage/medical/technology/mappingitem/update/delete
def get_list_key(value_list, key):
    for i in value_list:
        return i[key]

#判断提取值是否有idgi
def get_id_list(id_list):
    new_list = []
    for i in id_list:
        new_list.append(i['id'])
    print(new_list)
    return new_list


def get_typename():
    return "测试"+fake.name()+"类别"


def get_shiftname():
    return "测试"+fake.name()+"班次"


# 获取接口返回为数组时的内容，通过key返回对应value（key表示字段名称）
# bedsideSettlement.yml/app-billing/inPatient/charge/supplementMedicine/valid使用
def get_content_json_value(value_list, key):
    key = str(key)
    for i in value_list.keys():
        if key == i:
            return value_list[i]



# 判断接口返回的值是否为空，空的话返回true,使用skipIf跳过用例
def get_data_isnull(data):
    print(data)
    if data==[]:
        return True
    else:
        return False
# 判断接口返回的值是否为0，空的话返回false,使用skipIf跳过用例
def get_data_iszero(data):
    print(data)
    if data==0:
        return False
    else:
        return True

def create_name():
    name = genenate_chinese_name.create_name()
    return name


# 毫秒转化为日期,bedsideSettlement.yml/app-billing/inPatient/charge/list使用
def get_date_change(timeStamp):
    t1 = float(timeStamp) / 1000
    t2 = time.localtime(t1)
    t3 = time.strftime("%Y-%m-%d %H:%M:%S", t2)
    t4 = t3.split(" ")[0]
    return t4


# 结算的方式是否是现金，不是返回true
def get_pay_status(statusType):
    if statusType != "FH0085.01":
        return True
    else:
        return False


# 当月最后一天
def last_day_of_month():
    year = datetime.date.today().year
    month = datetime.date.today().month
    weekDay, monthCountDay = calendar.monthrange(year, month)
    lastDay=datetime.date(year,month,day=monthCountDay)
    return str(lastDay)


# 获取当前时间戳
def get_endtimestamp():
    cur_time = time.time()
    timestamp = int(round(cur_time - cur_time % 86400 +57599))*1000
    return timestamp


def get_starttimestamp():
    cur_time = time.time()
    timestamp = int(round(cur_time - cur_time % 86400)) * 1000
    return timestamp


# 获取当前时间戳
def get_timestamp():
    ctime = int(round(time.time() * 1000))
    return ctime

def slice(char):
    return char[8: 18]

if __name__ == '__main__':
    print(create_name())
    print(get_date())


