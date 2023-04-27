#! /usr/bin/env python
# -*- coding: utf-8 -*-

import config
import urllib
import requests
import random



# import json


# 获取实例列表
def get_instance_list(group, version):
    registry_address = config.get_env_variables["registry.address"]
    registry_namespace_id = config.get_env_variables["registry.namespace.id"]

    # 获取服务列表
    get_service_list = "/nacos/v1/ns/catalog/services"
    full_request_url = registry_address + get_service_list
    params = {
        "serviceNameParam": group,
        "groupNameParam": "",
        "pageSize": 10,
        "pageNo": 1,
        "namespaceId": registry_namespace_id
    }
    request_data = urllib.parse.urlencode(params)
    response = requests.get(url=full_request_url, params=request_data)
    # print(response.text)
    service_list = response.json()["serviceList"]
    service = ""
    for i in service_list:
        # 按照providers匹配
        if "providers" in i["name"] and version in i["name"]:
            service = i
            break
    # 请求实例的地址
    request_url = "/nacos/v1/ns/catalog/instances"
    full_request_url = registry_address + request_url
    try:
        params = {
            "serviceName": service["name"],
            "clusterName": "DEFAULT",
            "groupName": config.get_env_variables["groupName"],
            "pageSize": 10,
            "pageNo": 1,
            "namespaceId": registry_namespace_id
        }
    except Exception:
        raise Exception(f"服务ip获取失败，建议登陆nacos查看注册情况: 请求接口返回值{ service if service else '空' }")
    request_data = urllib.parse.urlencode(params)
    response = requests.get(url=full_request_url, params=request_data)
    instance_list = response.json()["list"]
    return instance_list


# 随机返回实例, 里面有ip和port
def get_service_instance(group, type, version="1.0.0"):
    instance_list = get_instance_list(group, version)
    # print(instance_list)
    #  随机选择一个实例
    instance = random.choice(instance_list)
    # print("应用" + group + "的ip为: " + instance["ip"])
    # print("应用" + group + "的port为: " + str(instance["port"]))
    print(instance["ip"])
    return instance[type]


if __name__ == '__main__':
    ip_list = get_service_instance("hbos-osc", "ip")
    print(ip_list)