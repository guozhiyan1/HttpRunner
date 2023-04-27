import faker
import random
import string
from tools import genenate_chinese_name
import threading
import json
from tools import gmc_mysql, generate_date, generate_run_sql


fake = faker.Faker(locale='zh_CN')
thread_local = threading.local()


def get_number(n):
    new_number = ''.join(random.sample('1123456789', n))
    return new_number

def get_date(**kwargs):
    """
    "%Y-%m-%d"
    "%Y-%m-%d %H:%M:%S"
    "%Y-%m-%dT%H:%M:%S.000Z"
    add_date=None
    delete_date=None
    """
    return generate_date.getdate(**kwargs)


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
        "card_number": fake.ssn(min_age=18, max_age=90),   #身份证号
        "inhospital_id": int(get_number(10)),
        "globelpatient_id": int(get_number(10)),
        "medicare_card": get_number(10),    #就诊卡号
        "patient_id": int(get_number(10)),   #registerId
        "telephone": fake.phone_number(),
        "medicare_number": fake.phone_number(),   #medical_record_no病历号
        "inpatient_no": get_number(10),
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
        "bed_patient_relation_id": int(get_number(8)),
        "order_id": int(get_number(8)),
        "master_patient_index": get_random_string(32),
        "user_id": 3142,
        "user_name": "医快一7",
        "apply_center_id": int(get_number(8)),
        "apply_id": int(get_number(8)),
        "inspect_id": int(get_number(8)),
        "apply_item_id": int(get_number(8)),
        "usageId": 1,
        "usageName": "口服",

        "nurse_patient_real_time_status_id": int(get_number(8)),
        "patientId": get_number(8),        ##患者就诊ID，就诊表主键
        "out_dept_id": 99897828604,      ##城站自动化测试门诊id
        "out_dept_name": "城站自动化测试门诊",
        "current_block_id": 99897828630,   ##诊区id
        "current_block_name": "自动化诊区",
        "today_date": get_date(number=0),    ##当天日期
        "encounter_date": get_date(number=1)+'.035',       ##接诊日期
        "medical_record_id1": int(get_number(7)),        ##biz_out_medical_record_content表“现病史”主键id
        "medical_record_id2": int(get_number(7)),        ##biz_out_medical_record_content表“主诉”主键id
        "medical_record_id3": int(get_number(7)),        ##biz_out_medical_record_content表“西医”主键id
        "medical_sign": int(get_number(7)),               ##biz_out_medical_record_info表患者病历体征数据主键id
        "order_id1": int(get_number(7)),                  ##biz_outpatient_order医嘱主键id
        "order_id2": int(get_number(7)),
        "order_id3": int(get_number(7)),
        "order_id4": int(get_number(7)),
        "order_id5": int(get_number(7)),
        "order_id6": int(get_number(7)),
        "order_id7": int(get_number(7)),
        "order_id8": int(get_number(7)),
        "nurse_surgery_id": int(get_number(6)),   ##手术医嘱表主键
        "surgery_order_id": int(get_number(10)),  ##手术医嘱id
        "surgery_id": int(get_number(5)),          ##biz_surgery_manage表主键id,手术号,手术相关需要用到的主键均复用
        "surgery_apply_no": int(get_number(9)),    ##biz_surgery_manage手术申请单号
        "surgery_apply_date": get_date(add_date=1)+" 08:00:00",  ##biz_surgery_manage拟手术时间2021-02-02 08:00:00
        "surgery_date": get_date(number=1),        ##手术申请时间：2021-01-27 14:55:00
        "anaesthesia_id": int(get_number(4)),      ##麻醉相关主键id
        "diagnosis_id": int(get_number(7)),         ##biz_out_diagnosis表诊断主键id
        "apply_inspect_item_id": int(get_number(8)),
        "gmc_date": generate_date.getdate(number=1)+".000",
        "schedule_id": int(get_number(8)),
        "resource_id": get_number(8),
        "dayweek_name": "星期日",
        "dayweek_code": "FH0035.07",
        "dayweek_number": "7",
        "resource_date": generate_date.getdate(),
        "resource_tomorrow_date":generate_date.getdate(add_date=1),
        "register_type_id": 64,
        "register_type_name": "自动化普通",
        "invoice_id":int(get_number(4)),     # 票据id,biz_invoice_register
        "invoice_date": get_date(number=1),  # 票据日期
        "settle_id": int(get_number(5)),     #结算id,biz_inhospital_settle_invoice
        "incharge_detail_id":int(get_number(8)),   ##住院费用明细id,biz_patient_charge_details
        "order_set_mainId": int(get_number(5)),  ##医嘱套餐模板类主键id
        "order_set_id": int(get_number(5)),  ##医嘱套餐模板主键id
        "order_set_itemId": int(get_number(7)),  ##医嘱套餐明细主键ID
        "order_set_name": "测试套餐" + genenate_chinese_name.create_name(),
        "order_set_model_name": "测试套餐模板" + genenate_chinese_name.create_name(),
        "patientId_history": int(get_number(7)),  ##历史就诊记录ID
        "orderId_history": int(get_number(7)) , ##历史医嘱ID
        "outpatient_charge_detail_id":int(get_number(8)),
        "prescription":int(get_number(5)),
        "prescription_detail_id":int(get_number(5)),
        "districtId": 2,  ##院区ID
        "material_item_name": 'W-材料',
        "plan_name":get_random_string(5),
        "schedule_rule_id1":int(get_number(5)),
        "schedule_rule_id2": int(get_number(5)),
        "schedule_rule_id3": int(get_number(5)),
        "schedule_rule_id4": int(get_number(5)),
        "schedule_rule_id5": int(get_number(5)),
        "schedule_rule_id6": int(get_number(5)),
        "schedule_rule_id7": int(get_number(5)),
        "set_type": 1  ##套餐所属类型：门诊1  住院2
    }
    thread_local.dict = dicts
    return dicts


sql_data_dicts = get_patient_data()


if __name__ == '__main__':
    print(sql_data_dicts)







