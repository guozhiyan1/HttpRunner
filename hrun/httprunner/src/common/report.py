#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/3/2 1:18 下午
# @Author  : 潇鸣 (lvzhengyong@alibaba-inc.com)
# @file    : report.py

import json
from datetime import datetime
import re



def strmake(str):
    print(str.group())
    keystr = "\'{}\'".format(str.group())
    return keystr



def get_result(summary):
    start_at_timestamp = summary["time"]["start_at"]
    utc_time_iso_8601_str = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
    summary["time"]["start_datetime"] = utc_time_iso_8601_str

    # 用指定的内容，替换正则匹配的内容，也可以指定替换次数
    result = re.sub('LazyString(.+?)\)', strmake, str(summary))
    return result


def thanos_report(result=''):
    data = {
        "testPass": result['stat']['teststeps']['successes'],
        "testName": "集成测试",
        "testAll": result['stat']['teststeps']['total'],
        "testFail": result['stat']['teststeps']['failures'],
        "beginTime": result['time']['start_datetime'],
        "totalTime": result['time']['duration'],
        "testSkip": result['stat']['teststeps']['skipped'],
        "testResult": []
    }

    for res in result['details'][0]['records']:

        a = {
            "className": res['name'],
            "methodName": "testDemo",
            "description": res['attachment'],
            "spendTime": "0ms",
            "status": res['status'],
            "log": {}
        }

        for log in res['meta_datas']['data']:
            # a['log'].append(log)
            # a['log']=log
            a['log']['data'] = log
            # for title in log:
            #     str="{0} {1}".format(title,log[title])
            #
            #     a['log'].append(str.replace("\\n",""))
            # a['log'].append(str(log[title]))
        data['testResult'].append(a)
    print("---" * 200)
    print(data)
    print(json.dumps(data))
    print("---" * 200)

if __name__ == '__main__':
    pass
    #
    # # c = re.compile(r'LazyString(.+?)\)')
    #
    # res='''
    # 'validators': {
    #     'validate_extractor': [{
    #         'comparator': 'equals',
    #         'check': 'status_code',
    #         'check_value': 200,
    #         'expect': LazyString($expected_status_code),')check_value': 200,
    # 'expect_value': 200,
    # 'check_result': 'pass'
    # 'expect': LazyString($expected_status_code),
    # 'expect': LazyString($expected_status_code),
    # },
    # '''
    #
    # # 用指定的内容，替换正则匹配的内容，也可以指定替换次数
    # ret = re.sub('LazyString(.+?)\)',strmake,res)
    #
    # print(ret)