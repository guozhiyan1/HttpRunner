# -*- coding: utf-8 -*-
# @File  : qiangzhiqiantui.py
# @Date  : 2020-08-27
# @Author: wb-zjm733140

import json
from copy import deepcopy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from requests import post


class QianTui:

    def __init__(self, zhouqihao, account_no=None, sign_type=0, env='test'):
        self.url = 'http://127.0.0.1:10000/agent/medicare/client/invokeDllMethod'
        self.zhouqihao = zhouqihao
        self.account_no = account_no
        self.sign_type = sign_type
        self.env = env

    def get_yibao_msg(self, **kwargs):
        data = {
            'medicareType':'HZSiInterface',
            'invokeMethodName':'BUSINESS_HANDLE',
            'outputPos':1,
            'params':None,
            'registerId':1,
            'methodId':1,
            'orgId':2
        }
        bus_type = kwargs.get('bus_type', 2)  # 1 对账， 2签退
        account_no = kwargs.get('account_no')
        if bus_type == 1:
            # 对账报文，默认0.00进行对账
            yiliaofei = kwargs.get('yiliaofei', '0.00')
            jijin = kwargs.get('jijin', '0.00')
            xianjin = kwargs.get('xianjin', '0.00')
            params = {
                '0':f'1100^1001^{account_no}^{self.zhouqihao}|330000^0200827000250^0^{yiliaofei}|{jijin}|{xianjin}|^1^'}
            data['params'] = params
        else:
            params = {'0':f'9110^1001^{account_no}^{self.zhouqihao}|^0200826000006^0^^1^'}
            data['params'] = params

        return data

    def duizhang_request(self, msg):
        res_dict = post(self.url, json.dumps(msg)).json()
        res_msg = res_dict.get('body', dict()).get('output')
        print(f'对账请求出参：{res_msg}')
        duizhang_jine = res_msg.split('^')[2].split('|')[1:]
        jine_list = list()
        for index, jine in enumerate(duizhang_jine):
            if index == 3:
                break
            qian, hou = jine.split('.')
            hou = hou.ljust(2, '0')
            jine = f'{qian}.{hou}'
            jine_list.append(jine)

        return jine_list[0], jine_list[1], jine_list[2], res_dict

    def qiantui_request(self, msg):
        res_dict = post(self.url, json.dumps(msg)).json()
        res_msg = res_dict.get('body', dict()).get('output')
        print(f'签退请求出参：{res_msg}')

        return res_dict

    def qiantui(self):
        # 数据库连接url
        if self.env == 'test':
            DB_CONNECT_STRING = "mysql+pymysql://seenew:ycnuWp_02@so@rm-bp1r017v4u82i103kko.mysql.rds.aliyuncs.com/medicare_platform_db"
        else:
            self.env = 'dev'
            DB_CONNECT_STRING = "mysql+pymysql://xnyl:test123456@rm-bp1qg2zx7l454lq46xo.mysql.rds.aliyuncs.com/medicare_platform_db"

        # 创建引擎
        engine = create_engine(DB_CONNECT_STRING, echo=False)

        # 自动映射
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        # 仅能对市医保，浙一账号进行对账签退，失败请手动操作

        # 获取指定类user表 --> user实体类
        biz_invoke_user_account = Base.classes.biz_invoke_user_account
        mysession = sessionmaker(bind=engine)()

        # 获取医保账号， 默认取签到类型为门诊
        account_no_query = mysession.query(biz_invoke_user_account).filter(
            biz_invoke_user_account.busss_cycle_number == self.zhouqihao and biz_invoke_user_account.sign_type ==
            self.sign_type and biz_invoke_user_account.active == 1).first()
        if account_no_query is None:
            raise Exception(f'未获取到签到记录,周期号：环境{self.env}，签到类型{self.sign_type}, 周期号：{self.zhouqihao}')
        if self.account_no is None:
            self.account_no = account_no_query.account_no
            print(f'获取到的account_no为{self.account_no}')

        # 获取费用,拼接对账签退报文
        print('1、获取费用,拼接对账报文')
        duizhang_args = {'bus_type':1, 'account_no':self.account_no}
        duizhang_msg = self.get_yibao_msg(**duizhang_args)
        yiliaofei, jijin, xianjin, res_dict = self.duizhang_request(duizhang_msg)
        duizhang_args['yiliaofei'] = yiliaofei
        duizhang_args['jijin'] = jijin
        duizhang_args['xianjin'] = xianjin
        duizhang_msg = self.get_yibao_msg(**duizhang_args)
        print(f'对账报文为：{duizhang_msg}')

        # 签退报文
        qiantui_args = {'bus_type':0, 'account_no':self.account_no}
        qiantui_msg = self.get_yibao_msg(**qiantui_args)
        print(f'签退报文为：{qiantui_msg}')

        # 进行对账
        i = 0
        while True:
            print(f'第{i + 1}次尝试对账、签退')
            self.duizhang_request(duizhang_msg)
            res_dict = self.qiantui_request(qiantui_msg)
            output = res_dict.get('body', dict()).get('output')
            if output.__contains__('系统没有检索到业务周期号'):
                account_no_query.busss_cycle_number = ''
                account_no_query.sign_status = 0
                break
            i += 1

        print('签退成功，请尝试重新签到')
        # 提交
        mysession.commit()
        # 关闭session
        mysession.close()

        pass


if __name__ == '__main__':
    # QianTui('20200928162203-1001-jfzx-dev-3917', env='dev').qiantui()
    QianTui('20201117105805-1001-00099009-4119', env='dev').qiantui()
