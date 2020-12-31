#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/3/3 5:08 下午
# @Author  : 潇鸣 (lvzhengyong@alibaba-inc.com)
# @file    : innerapi.py
import time
import json
import hmac
import base64
from hashlib import sha1
import urllib.request
import urllib.parse

import os



# def _gen_alert_sign(method, secret, string):
#     para = urllib.parse.quote(string)
#     para = method + '&%2F&' + para
#     para = para.encode('utf-8')
#     SECRET_KEY = bytes(secret + '&', encoding='utf-8')
#     sign = hmac.new(SECRET_KEY, para, sha1).digest()
#     sign = base64.b64encode(sign)
#     sign = urllib.parse.quote(sign)
#     sign = sign.replace('/', '%2F')
#     return sign
#
#
# def get_para(params):
#     para = [(k, params[k]) for k in sorted(params.keys())]
#     para = urllib.parse.urlencode(para)
#     dicts = {"!": "%21", "*": "%2A", "\'": "%27", "(": "%28", ")": "%29", "+": "%20", "[": "%5B"}
#     for key in dicts:
#         para = para.replace(key, dicts[key])  # 空格特殊
#     return para


def get_secret(params):
    for k in list(params.keys()):
        if not params[k]:
            del params[k]
    if params.get("app"):
        secret = os.environ.get("rubic_secret")
        params['timestamp'] = int(round(time.time() * 1000))
    elif params.get("request_type"):
        secret = os.environ.get(params.get("request_type") + "_secret")
        params.pop("request_type")
        params['ts'] = int(time.time())
    else:
        secret = os.environ.get("innerapi_secret")
        params['ts'] = int(time.time())


    return params, secret


# def request_get(method, params):
#     params, secret = get_secret(params)
#     para = get_para(params)
#     sign = _gen_alert_sign(method, str(secret), para)
#     return sign
#
#
# def request_post(getParams, postParams,body_is_sign=True):
#     sign=''
#     if body_is_sign:
#         getParams, secret = get_secret(getParams)
#         Params={**getParams, **postParams}
#         para = get_para(Params)
#         sign = _gen_alert_sign("POST", str(secret), para)
#     else:
#         getParams, secret = get_secret(getParams)
#         sign = _gen_alert_sign("POST", str(secret))
#     return sign



def _gen_alert_sign(method, secret, string):
    para = urllib.parse.quote(string)
    para = method + '&%2F&' + para
    para = para.encode('utf-8')
    SECRET_KEY = bytes(secret + '&', encoding='utf-8')
    sign = hmac.new(SECRET_KEY, para, sha1).digest()
    sign = base64.b64encode(sign)
    sign = urllib.parse.quote(sign)
    sign = sign.replace('/', '%2F')
    return sign


def get_para(params):
    para = [(k, params[k]) for k in sorted(params.keys())]
    para = urllib.parse.urlencode(para)
    dicts = {"!": "%21", "*": "%2A", "\'": "%27", "(": "%28", ")": "%29", "+": "%20"}
    for key in dicts:
        para = para.replace(key, dicts[key])  # 空格特殊
    return para

def request_get(requests):
    getParams=requests.get("params")
    requests['params']["ts"] = int(time.time())
    if requests['params'].get("request_type", None):
        secret = os.environ.get(requests['params'].get("request_type") + "_secret")
    else:
        secret = os.environ.get("innerapi_secret")
        # getParams,secret=get_secret(getParams)
    para = [(k, getParams[k]) for k in sorted(getParams.keys())]
    para = urllib.parse.urlencode(para).replace('+', '%20').replace('%27', '%22')  # 空格特殊
    sign = _gen_alert_sign("GET", str(secret), para)
    # url="{0}?{1}&sign={2}".format(uri, para, sign)
    requests['params']['sign']=sign
    return sign


def request_post(requests):
    requests['data'] = requests.get("data", {})
    body_is_sign=requests['params'].get("body_is_sign",1)
    requests['params']["ts"]=int(time.time())
    if requests['params'].get("request_type",None):
        secret = os.environ.get(requests['params'].get("request_type") + "_secret")
    else:
        secret = os.environ.get("innerapi_secret")
    if 'pdata' in requests['data']:  # 处理post参数中pdata
        postParams = {'pdata': json.dumps(requests['data']['pdata'])}
        requests['data'] = postParams  # 改变request里面的值

    if body_is_sign :
        data={}
        if requests.get("data",{}):
            data=requests["data"]
        if requests.get("json",{}):
            data=requests["json"]
        Params = {**requests['params'], **data}
    else:
        Params=requests['params']
    para = [(k, Params[k]) for k in sorted(Params.keys())]
    para = urllib.parse.urlencode(para).replace('+', '%20').replace('%27', '%22')  # 空格特殊
    sign = _gen_alert_sign("POST", str(secret), para)
    # requests['params']['sign']=sign
    return sign
