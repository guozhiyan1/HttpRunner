import os
import random
import string
import time
import datetime
from httprunner import logger
from tools.IDCARD.idcard_provide import IDCardProvide
from tools import gmc_mysql, generate_date, generate_run_sql
import faker
from data.sql_dict import *
from data import basic_dict

BASE_URL = "http://127.0.0.1:5000"
fake = faker.Faker(locale='zh_CN')
sql_data_dicts = basic_dict.sql_data_dicts


def sum_two(m, n):
    return m + n


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
    for i in value_list:
        if i[key] == value:
            return str(i[result])


def get_id_list(id_list):
    new_list = []
    for i in id_list:
        new_list.append(i['id'])
    print(new_list)
    return new_list


if __name__ == '__main__':
    print(get_date())
