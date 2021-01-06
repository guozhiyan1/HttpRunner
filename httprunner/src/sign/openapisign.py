#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/3/3 4:26 下午
# @Author  : 潇鸣 (lvzhengyong@alibaba-inc.com)
# @file    : openapisign.py


import urllib
import urllib.request
import urllib.error
import urllib.parse
import time
import base64
import hmac
import uuid
from hashlib import sha1
import os


# from aliyunsdkcore.auth.rpc_signature_composer import get_signed_url

#采用变准sdk方式签名
# def sign_sdk(params):
#     print("{0}{1}{2}".format("="*20,params,"="*20))
#     ak, secret = '', ''
#     # 获取  ak secret 通过环境变量提取
#     try:
#         ak = os.environ.get("openapi_ak")
#         secret = os.environ.get("openapi_secret")
#     except Exception as e:
#         print(e)
#         print("获取环境变量出错")
#         exit(0)
#
#     # 删除values为空的键值
#     for k in list(params.keys()):
#         if params[k] == "":
#             del params[k]
#
#     get_signed_url(params,ak,secret,'json','GET')


# #签名
def sign(parameters,secret=''):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])  # 使用get请求方法
    bs = secret + '&'
    bs = bytes(bs, encoding='utf8')
    stringToSign = bytes(stringToSign, encoding='utf8')
    h = hmac.new(bs, stringToSign, sha1)
    # 进行编码
    signature = base64.b64encode(h.digest()).strip()
    return signature


def percent_encode(encodeStr):
    encodeStr = str(encodeStr)
    res = urllib.request.quote(encodeStr)
    dicts = {"!": "%21", "*": "%2A", "\'": "%27", "(": "%28", ")": "%29", "+": "%20"}
    for key in dicts:
        res = res.replace(key, dicts[key])  # 空格特殊
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    res = res.replace('/', '%2F')
    return res


# 构建除共公参数外的所有URL
def make_signature(params):
    '''
    :param params: 签名参数
    '''
    ak,secret='',''
    # 获取  ak secret 通过环境变量提取
    try:
        ak = os.environ.get("openapi_ak")
        secret = os.environ.get("openapi_secret")
    except Exception as e:
        print(e)
        print("获取环境变量出错")
        exit(0)

    # 删除values为空的键值
    for k in list(params.keys()):
        if params[k] == "":
            del params[k]

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    parameters = {
        'Format': 'JSON',
        'SignatureVersion': '1.0',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'Timestamp': timestamp,
        'AccessKeyId': ak
    }
    params.update(parameters)
    signature = sign(params,secret)
    params['Signature'] = signature

if __name__ == '__main__':
    pass