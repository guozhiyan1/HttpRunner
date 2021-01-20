import faker
import random
import string
from data import genenate_chinese_name
import threading
import json

fake = faker.Faker(locale='zh_CN')
thread_local = threading.local()


def getcard():
    newstring = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    return "0zdh" + newstring


def get_number(n):
    new_number = ''.join(random.sample('0123456789', n))
    return new_number


def get_random_string(str_len):
    random_char_list = []
    for _ in range(str_len):
        random_char = random.choice(string.ascii_letters + string.digits)
        random_char_list.append(random_char)

    random_string = ''.join(random_char_list)
    return random_string


def get_card_number():
    return fake.ssn(min_age=18, max_age=90)


def get_patient_data():
    bed_number = get_number(6)
    dicts = {
        "patient_name": "测试"+genenate_chinese_name.create_name(),
        "card_number": fake.ssn(min_age=18, max_age=90),
        "inhospital_id": get_number(8),
        "globelpatient_id": get_number(8),
        "medicare_card": get_number(8),
        "patient_id": get_number(8),
        "telephone": fake.phone_number(),
        "medicare_number": fake.phone_number(),
        "inpatient_no": get_number(8),
        "area_id": 99897828607,
        "area_name": "城站消化血液科自动化病区",
        "area_name_pinyin": 'chengzhanxiaohuaxueyekezidonghuabingqu',
        "department_id": 99897828605,
        "department_name": "城站自动化消化血液科",
        "org_id": 1,
        "room_id": 3161,
        "location_id": 99897828609,
        "bed_type_id": 2995,
        "bed_id": bed_number,
        "bed_number": bed_number,
        "medical_record_no": get_number(10),
        "bed_patient_relation_id": get_number(10),
        "order_id": int(get_number(8)),
        "master_patient_index": get_random_string(32),
        "user_id": 3142,
        "user_name": "医快一7",
        "apply_center_id": int(get_number(8)),
        "apply_id": int(get_number(8)),
        "apply_item_id": int(get_number(8)),
        "usageId": 1,
        "usageName": "口服",
        "nurse_patient_real_time_status_id": int(get_number(8))
    }
    thread_local.dict = dicts
    return dicts


sql_data_dicts = get_patient_data()


if __name__ == '__main__':
    print(sql_data_dicts)







