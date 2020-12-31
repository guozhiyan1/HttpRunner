#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/3/25 4:38 下午
# @Author  : 潇鸣 (lvzhengyong@alibaba-inc.com)
# @file    : tools.py

import json

def getres_status(data):
    '''
    专门处理后付费 openapi实例状态
    {
    "TotalCount": 1,
    "MultiCarrierInstanceCount": 0,
    "PageSize": 10,
    "RequestId": "779A1914-7F6D-490B-940C-2951F67834A0",
    "PageNumber": 1,
    "EnsServices": {
        "EnsService": [
            {
                "Status": [
                    {
                        "Status": "Running",
                        "Count": 1
                    }
                ],
                "EnsServiceName": "创建边缘服务",
                "CreatTime": "2020-03-25T07:01:36Z",
                "InstanceSpec": "ens.sn1.stiny",
                "EnsServiceId": "ens-202003251501358Mz1gy",
                "NetLevel": "Big",
                "Memory": 2,
                "BuyResourcesDetail": [
                    {
                        "NetDistrictCode": "100106",
                        "InstanceInfo": [
                            {
                                "InstanceCount": 1,
                                "Carrier": "telecom"
                            }
                        ]
                    }
                ],
                "SystemDisk": 20,
                "Cores": 1,
                "ImageName": "centos_7_03_64_20G_alibase_20171211",
                "SchedulingStrategy": "Disperse",
                "DataDisk": 40,
                "InternetMaxBandwidthOut": 40,
                "ImageId": "centos_7_03_64_20G_alibase_20171211",
                "SchedulingPriceStrategy": "PriceHighPriority"
            }
        ]
    },
    "Code": 0
}
    :param data:
    :return:
    '''

    status=''

    for i in data['EnsServices']['EnsService']:
        if i['Status'][0]['Status'] != 'Running':
            status = i['Status'][0]['Status']
        else:
            status = i['Status'][0]['Status']
            break
    return status


def get_post_status(data):
    '''
    [{
            "status": 600,
            "resource_name": "20200709cn888-1",
        },
        {
            "status": 600,
            "resource_name": "cn1106-6",
            "data_disk": 122880,

        }]
    '''
    status=''

    for i in data:
        if i['status'] == 600:
            status = i['status']
        else:
            status = i['status']
            break
    return status


if __name__ == '__main__':
    data = {"TotalCount": 1, "MultiCarrierInstanceCount": 0, "PageSize": 10,
            "RequestId": "0DE13413-0478-4C86-8AE3-4CE18C6D1627", "PageNumber": 1, "EnsServices": {"EnsService": [
            {"Status": [{"Status": "ImageDownloading", "Count": 1}], "EnsServiceName": "创建边缘服务",
             "CreatTime": "2020-03-25T09:52:25Z", "InstanceSpec": "ens.sn1.stiny",
             "EnsServiceId": "ens-20200325175224E52LMj", "NetLevel": "Big", "Memory": 2, "BuyResourcesDetail": [
                {"NetDistrictCode": "100106", "InstanceInfo": [{"InstanceCount": 1, "Carrier": "telecom"}]}],
             "SystemDisk": 20, "Cores": 1, "ImageName": "centos_7_03_64_20G_alibase_20171211",
             "SchedulingStrategy": "Disperse", "DataDisk": 40, "InternetMaxBandwidthOut": 40,
             "ImageId": "centos_7_03_64_20G_alibase_20171211", "SchedulingPriceStrategy": "PriceHighPriority"}]},
            "Code": 0}

