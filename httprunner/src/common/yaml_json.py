"""
josn文件解析为yaml
"""
import yaml


def to_yaml(json_dict):
    """
    change json to yaml
    :param json_dict:
    :return:
    """
    return yaml.safe_dump(json_dict, default_flow_style=False)


# def to_json(yaml_dict):
#     return yaml.safe_load(yaml_dict)


def get_params(json_dict):
    """
    将请求参数打印为case中可直接使用的参数
    :param json_dict:
    :return:
    """
    for key in json_dict:
        print(f'{str.capitalize(key[0]) + key[1:]}: "{json_dict[key]}"')
    print()
    for key in json_dict:
        strs = str.capitalize(key[0]) + key[1:]
        print(f'{strs}: "${strs}"')


json_file = [
  {
    "request": {
      "case_id": "test_v3order_001",
      "case_name": "v3order接口创建实例",
      "description": "创建实例",
      "waittime":3,
      "retry_conut":1,
      "priority": 0,
      "method": "post",
      "action": "/v3/order",
      "type": "ens_innerapi",
      "parameters": {
        "getParams":"",
        "postParams":{
        "order_type": "BUY",
        "buyer_id": 1081314188858019,
        "order_details": [
        {
            "password": "VhHLJ*P2RNfN",
            "internet_vlan": 800,
            "spec_type": 1,
            "amount": 1,
            "with_internet_ip": True,
            "bandwidth_mode": 1,
            "bandwidth_in": 0,
            "bandwidth_out": 0,
            "system_disk": {
                "device_type": "file",
                "size": 20480
            },
            "start_time": 1556197437,
            "end_time": 1956639999,
            "ens_region_id": "cn-shanghai-telecom-3",
            "image_id": "centos_6_08_64_20G_alibase_20171208",
            "spec_name": "ens.sn1.stiny"
        }
        ]
        }
      }
    },
    "expect": {
      "code": 0,
      "msg": "成功"
    },
    "response": {
      "code": 0,
      "msg": "{{ context.reslut.test_v3order_001.msg }}"
    }
  },
  {
    "request": {
      "case_id":"test_v3order_002",
      "case_name": "获取指定实例状态",
      "description": "创建实例",
      "priority": 0,
      "method": "get",
      "action": "/v1/instance",
      "type": "ens_innerapi",
      "waittime":30,
      "retry_conut":3,
      "parameters": {
        "getParams": {
          "instance_id": "{{ context.reslut.test_v3order_001.data }}",
          "ali_uid": "1081314188858019",
          "page": "1"
        },
        "postParams": ""
      }
    },
    "expect": {
      "code": 0,
      "msg": "成功",
      "data": [{"status":"running"}]
    },
    "response": {
      "code": 0,
      "msg": "成功",
      "data": [{"status":"{{ context.reslut.test_v3order_002.data[0].status }}"}]
    }
  }
]


get_params(json_file)
# print(to_yaml(json_file))
