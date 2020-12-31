#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/3/2 1:18 下午
# @Author  : 潇鸣 (lvzhengyong@alibaba-inc.com)
# @file    : report.py

import os
import re
from jinja2 import Environment, FileSystemLoader
from httprunner.src.common import util


def strmake(str):
    print(str.group())
    keystr = "\'{}\',".format(str.group())
    return keystr


def get_result(summary):
    # 用指定的内容，替换正则匹配的内容，也可以指定替换次数
    result = re.sub('LazyString(.+?)\),', strmake, str(summary))
    return result

def generate_html(data):
    tmlp_path=os.path.join(util.get_rootpath(), "httprunner/report/html")
    res_path=os.path.join(util.get_rootpath(), "reports", "new_results.html")
    print(tmlp_path)
    env = Environment(loader=FileSystemLoader(tmlp_path))  # 加载模板
    template = env.get_template('thanos_report_local.html')

    with open(res_path, 'w') as fout:
        html_content = template.render(data=eval(data))
        fout.write(html_content)  # 写入模板 生成html

if __name__ == '__main__':
    pass