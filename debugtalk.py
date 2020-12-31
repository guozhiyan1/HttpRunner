import os
import random
import string
import time
import datetime
from httprunner import logger
from tools.IDCARD.idcard_provide import IDCardProvide


BASE_URL = "http://127.0.0.1:5000"


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


# def alter_response_error(response):
#     # NameError
#     not_defined_variable


def gen_variables():
    return {
        "var_a": 1,
        "var_b": 2
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


def get_cancelHospitalizedRegister():
    ZHUYUAN_HUANZHE = [{"masterPatientIndex":"06cf01b2af9f469bb0b5813b492acf97","patientRegisterId":"21303","inhospitalPatientId":"5000088"},
{"masterPatientIndex":"7e583f7a1e7b426a8220f30cee8ba292","patientRegisterId":"21304","inhospitalPatientId":"5000089"},
{"masterPatientIndex":"2525d3cc38314498b4102550f5e24b7c","patientRegisterId":"21302","inhospitalPatientId":"5000090"},
{"masterPatientIndex":"29754572b6624e7c9c54a86f7edf8c71","patientRegisterId":"21305","inhospitalPatientId":"5000091"},
{"masterPatientIndex":"d8142d0027bb49ad90bb98664f2bf8d4","patientRegisterId":"21336","inhospitalPatientId":"5000121"},
{"masterPatientIndex":"8dad449c903d4f019565f3c53ea9f4d0","patientRegisterId":"21318","inhospitalPatientId":"5000095"},
{"masterPatientIndex":"18c078c9f35f430aae1b723a3527eeec","patientRegisterId":"21314","inhospitalPatientId":"5000093"},
{"masterPatientIndex":"003f05b6765a4c048be076dda55424bd","patientRegisterId":None,"inhospitalPatientId":"5000170"},
{"masterPatientIndex":"62870c4784a14cc2993933c074de5c4b","patientRegisterId":"21343","inhospitalPatientId":"5000128"},
{"masterPatientIndex":"cc70e96a4f894bcfb7dee7ce9dc0cca1","patientRegisterId":"21435","inhospitalPatientId":None},
{"masterPatientIndex":"2253734ca6414396baf20882269b1412","patientRegisterId":"21434","inhospitalPatientId":None},
{"masterPatientIndex":"6e949ef7ae9643ae91004ec78c140128","patientRegisterId":"21436","inhospitalPatientId":None},
{"masterPatientIndex":"204d32a03d46452f9794a9bb50a9ce5a","patientRegisterId":"21437","inhospitalPatientId":None},
{"masterPatientIndex":"53b1e482f39c4c268c711d2cbed09353","patientRegisterId":"21438","inhospitalPatientId":None},
{"masterPatientIndex":"8c514951e60047dd90d9179fba9ea48b","patientRegisterId":"17019","inhospitalPatientId":"4033870"},
{"masterPatientIndex":"ea4a37d304a54932bab1dad8df928ba3","patientRegisterId":"17628","inhospitalPatientId":"4037478"}]

    ZHUYUAN_HUANZHE =[{"masterPatientIndex": "550f547743614caa916ddc77c8fb6686", "patientRegisterId": "13802",
     "inhospitalPatientId": "196386"},{"masterPatientIndex": "e83b9337678e435bbe00e3e31f8ab17a", "patientRegisterId": "14255",
     "inhospitalPatientId": "196435"},{"masterPatientIndex": "f24dc286ba064979b3961e9a2e8497ca", "patientRegisterId": "14254",
     "inhospitalPatientId": "196436"},{"masterPatientIndex": "340f6ce5bd4e494a85b8adf46778c9e5", "patientRegisterId": "14253",
     "inhospitalPatientId": "196437"},{"masterPatientIndex": "f28cc17b6d5441cbb0b816cb8af7a0e9", "patientRegisterId": "14252",
     "inhospitalPatientId": "196438"},{"masterPatientIndex": "57f77510aa2141e490ce7c76becea769", "patientRegisterId": "14251",
     "inhospitalPatientId": "196439"},{"masterPatientIndex": "88ab0636ed234b1a8d7ff21bbe2b0f7c", "patientRegisterId": "14249",
     "inhospitalPatientId": "196441"}, {"masterPatientIndex": "1aa3e21017b94ceabca346856a5ea823", "patientRegisterId": "14248",
     "inhospitalPatientId": "196442"},{"masterPatientIndex": "c84056075e7342df8899dc4a083ca306", "patientRegisterId": "14247",
     "inhospitalPatientId": "196449"},{"masterPatientIndex": "ef16fdd04ac14704af9c471273269a5f", "patientRegisterId": "14245",
     "inhospitalPatientId": "196452"},{"masterPatientIndex": "a1dfaee46dce476a8f589863b335c68d", "patientRegisterId": "14243",
     "inhospitalPatientId": "196454"},{"masterPatientIndex": "8b300f807c444f3681b0dca97fda789b", "patientRegisterId": "14241",
     "inhospitalPatientId": "196455"},{"masterPatientIndex": "cf16e3865b794fcb8389b960f92c61b7", "patientRegisterId": "14246",
     "inhospitalPatientId": "196456"},{"masterPatientIndex": "0077020130264d5fad76cd2d23ccadc8", "patientRegisterId": "14259",
     "inhospitalPatientId": "196457"}]

    return ZHUYUAN_HUANZHE