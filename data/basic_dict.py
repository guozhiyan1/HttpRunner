import faker
import random
import string
from . import genenate_chinese_name
import threading

fake = faker.Faker(locale='zh_CN')
thread_local = threading.local()


def getcard():
    newstring = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    return "0zdh" + newstring


def get_number(n):
    new_number = ''.join(random.sample('0123456789', n))
    return new_number


def get_card_number():
    return fake.ssn(min_age=18, max_age=90)


def get_patient_data():
    dicts = {
        "patient_name": genenate_chinese_name.create_name(),
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
        "bed_id": get_number(6)
    }
    thread_local.in_hospital_id = dicts['inhospital_id']
    return dicts

sql_data_dicts = get_patient_data()



