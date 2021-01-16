import os
import random
import string
import time
import datetime
from httprunner import logger
from tools.IDCARD.idcard_provide import IDCardProvide
from tools import gmc_mysql
import faker
from data.basic_dict import sql_data_dicts
from data.newpatient import *
from data import basic_dict

BASE_URL = "http://127.0.0.1:5000"
fake = faker.Faker(locale='zh_CN')


def get_id_no():
    """
    随机生成一个年龄为14到90之间的身份证号
    :return: 身份证号
    """
    while True:
        # 部分挂号科室有挂号年龄限制，故生成身份证时取年龄为14到90
        card_no = IDCardProvide().create_idnum_all_elements()[0]
        city, birth, sex = IDCardProvide().resolution_idnum(card_no)
        birth_year = int(birth.split('-')[0])
        curr_year = datetime.date.today().year
        age = curr_year - birth_year
        if age <= 14 or age > 90:
            continue
        else:
            break

    return [card_no, f'huanzhe{card_no[-6:]}']


def get_base_url():
    return BASE_URL


def get_default_request():
    return {
        "base_url": BASE_URL,
        "headers": {
            "content-type": "application/json"
        }
    }


def sum_two(m, n):
    return m + n


def sum_status_code(status_code, expect_sum):
    """ sum status code digits
        e.g. 400 => 4, 201 => 3
    """
    sum_value = 0
    for digit in str(status_code):
        sum_value += int(digit)

    assert sum_value == expect_sum


def is_status_code_200(status_code):
    return status_code == 200


os.environ["TEST_ENV"] = "PRODUCTION"


def skip_test_in_production_env():
    """ skip this test in production environment
    """
    return os.environ["TEST_ENV"] == "PRODUCTION"


def sleep_time(i):
    for i in range(i):
        time.sleep(1)
        logger.log_info(f"前置方法暂停{i}秒")

def get_user_agent():
    return ["iOS/10.1", "iOS/10.2"]


def gen_app_version():
    return [
        {"app_version": "2.8.5"},
        {"app_version": "2.8.6"}
    ]


def get_account():
    return [
        {"username": "user1", "password": "111111"},
        {"username": "user2", "password": "222222"}
    ]


def get_account_in_tuple():
    return [("user1", "111111"), ("user2", "222222")]


def gen_random_string(str_len):
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


def teardown_hook_sleep_N_secs(response, n_secs):
    """ sleep n seconds after request
    """
    if response.status_code == 200:
        time.sleep(0.1)
    else:
        time.sleep(n_secs)


def hook_print(msg):
    print(msg)


def modify_request_json(request, os_platform):
    request["json"]["os_platform"] = os_platform


# def setup_hook_httpntlmauth(request):
#     if "httpntlmauth" in request:
#         from requests_ntlm import HttpNtlmAuth
#         auth_account = request.pop("httpntlmauth")
#         request["auth"] = HttpNtlmAuth(
#             auth_account["username"], auth_account["password"])


def alter_response(response):
    response.status_code = 500
    response.headers["Content-Type"] = "html/text"
    response.json["headers"]["Host"] = "127.0.0.1:8888"
    response.new_attribute = "new_attribute_value"
    response.new_attribute_dict = {
        "key": 123
    }

def alter_response_302(response):
    response.status_code = 500
    response.headers["Content-Type"] = "html/text"
    response.text = "abcdef"
    response.new_attribute = "new_attribute_value"
    response.new_attribute_dict = {
        "key": 123
    }




def get_token(token):
    #
    try:
        token = token['token_type'] + " " + token["access_token"]
    except Exception as e:
        logger.log_info("token  获取失败  %s %s" % (token, e))
    return token


def getdate():
    return time.strftime("%Y-%m-%d", time.localtime())


def getdateandtime(month=""):
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return today

def getTZdate():
    today = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.localtime())
    return today


def stamp():
    return time.time()


def getcard():
    newstring = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    return "0zdh" + newstring


def get_number(n):
    new_number = ''.join(random.sample('0123456789', n))
    return new_number


def get_name():
    return fake.name()


def get_card_number():
    return fake.ssn(min_age=18, max_age=90)


def get_sql_string(sql_string):
    new_sql = []
    for i in sql_string:
        i = globals()[i]
        new_sql += i
    return new_sql


def gmc_run_mysql(master_patient_index, bed_number, *args):
    run_sql = args
    run_sql = get_sql_string(run_sql)
    sql_data_dicts["master_patient_index"] = master_patient_index
    sql_data_dicts["bed_number"] = bed_number
    sql_data_dicts["bed_id"] = bed_number
    print(basic_dict.thread_local.in_hospital_id)

    for j in run_sql:
        for s in sql_data_dicts:
            j = j.replace(f"[{s}]", f"'{sql_data_dicts[s]}'")
        # gmc_mysql.get_database(j)
    return sql_data_dicts


def get_list_dict_value(value_list, key, value, result):
    for i in value_list:
        if i[key] == value:
            return str(i[result])


if __name__ == '__main__':
    print(gmc_run_mysql(gen_random_string(32), "add_bed"))
