import json
import os

root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0]
f1 = os.path.join(root_path, "all_sql_list.json")
f2 = os.path.join(root_path, "basic_sql_dict.json")


def get_json_sql_dict():
    with open(f1, 'r', encoding='utf8')as s:
        return json.load(s)


def get_json_dict():
    with open(f2, 'r', encoding='utf8')as s:
        return json.load(s)


def get_result_list(dict_key="apply_order_add"):
    json_sql_dict = get_json_sql_dict()
    json_data = get_json_dict()
    result_list = []
    for j in json_sql_dict[dict_key]:
        if j == "comment":
            pass
        else:
            k = json_data[j]
            for m in json_sql_dict[dict_key][j]:
                result_list.append(k[m])
    return result_list


# for i in get_result_list():
#     print(i)



