#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/3/4 2:43 下午
# @Author  : 潇鸣 (lvzhengyong@alibaba-inc.com)
# @file    : util.py
import configparser
import sys

from loguru import logger
import subprocess
import requests
import socket
# import paramiko
import json,time,os


def get_rootpath():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


def ping(ip):
    r = subprocess.call("ping -q -c2 %s > /dev/null" % ip, shell=True)
    return r == 0


def error(content):
    print ("\033[31m{0}\033[0m".format(content))


def success(content):
    print ("\033[32m{0}\033[0m".format(content))


def warn(content):
    print ("\033[33m{0}\033[0m".format(content))

def loadjson(filename):
    load_dict = ''
    # dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # dir_path = os.path.dirname(os.path.abspath(__file__))
    # dir_name = os.path.join(dir_path, "create_prm", filename)
    # print '文件路径:', dir_name
    with open(filename, "r") as load_f:
        load_dict = json.load(load_f)
        # print(load_dict)
    return load_dict

def write_file(context='', file_name=''):
    if context is None:
        return None
    if file_name == '':
        file_name=os.path.join(get_rootpath(),"data","uuid.txt")
        print(file_name)
    with open(file_name, "a+") as f:
        f.write("{0}\n{1}\n".format(context,"-"*100))
    return True

def read_file(filename):
    conx_list = []
    with open(filename, 'r') as f1:
        conx = f1.readlines()
    for x in conx:
        if x.rstrip('\n') == '' or x.startswith("#"):
            continue
        conx_list.append(x.rstrip('\n'))
    return conx_list


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



def run_cmd( cmd, with_sudo=False):
    """
    run cmd in another proccess
    """
    if with_sudo:
        cmd = 'sudo ' + cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = p.communicate()[0]
    if p.returncode != 0:
        print("失败")
        logger.debug("cmd:[%s],res=[%s]" % (cmd, res))
    return (res, p.returncode)


def pingcmd(ip):
    '''
    检查当前运行环境到指定ip地址ICMP协议是否正常
    :param ip:
    :return:
    '''
    cmdstr="ping -i 1 -W 1 %s  -c 1" % ip
    res=run_cmd(cmdstr,False)[1]
    logger.debug("cmd:[%s],res=[%s]" % (cmdstr,res))
    if res==0:
        return True
    return False

def httpget(ip='',port='',url=''):
    '''
    检查当前环境请求http状态吗返回200
    :param ip: ip地址
    :param port: 端口
    :param url: 完整url
    :return:
    '''
    if url != '':
        url=url
    else:
        url = "http://{}:{}".format(ip, port)
    res=requests.get(url)
    print(res.status_code)
    if res.status_code==200:
        return True
    return False

def check_port(ip, port, timeout=3):
    '''
    检查某个ip的某个端口是否存活
    :param ip:  ipv4地址
    :param port: 端口
    :param timeout: 超时时间
    :return:  探测存活返回Ture 反之False
    '''
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(int(timeout))
    try:
        sk.connect((ip, int(port)))
        return True
    except Exception as e:
        logger.info("ip:{0} port:{1} \n 错误原因:{2}".format(ip,port,str(e)))
    finally:
        sk.close()
    return False

#
# def ssh_check(ip,user='root',port=22,passwd='a123456789*'):
#     '''
#     ssh登录ip 默认密码a123456789*\端口22\用户root
#     :param ip: ip地址
#     :return: 成功返回True 反之False
#     '''
#     # 建立一个sshclient对象
#     ssh = paramiko.SSHClient()
#     # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         ssh.connect(ip, int(port), user, passwd, timeout=5)
#         return True
#     except Exception as e:
#         logger.info("ip:{0} port:{1} \n 错误原因:{2}".format(ip,port,str(e)))
#         return False
#     finally:
#         ssh.close()

def getConfig(section,option=None,items=None,file=''):
    '''
    eg:
    [test]     section=test
    user=root  option=user
    file 默认可以不传入  默认读取更目录下面config.ini文件
    result   root
    '''

    cf = configparser.ConfigParser()
    if file :
        config_file=file
    else:
        config_file='config.ini'
    configfile=os.path.join(get_rootpath(),config_file)
    if sys.platform.startswith('win'):
        cf.read(configfile, encoding='gbk')
    else:
        cf.read(configfile, encoding='utf-8')
    if items :
        result=cf.items(section)

    else:
        result=cf.get(section,option)

    print(dict(result))
    return dict(result)

def setConfig(section=None,option=None,values=None,file=None):
    '''
    eg:
    [test]     section=test
    user=root  option=user
    file 默认可以不传入  默认读取更目录下面config.ini文件
    result   root
    '''

    cf = configparser.ConfigParser()
    if file :
        config_file=file
    else:
        config_file='config.ini'
    configfile=os.path.join(get_rootpath(),config_file)
    if sys.platform.startswith('win'):
        cf.read(configfile, encoding='gbk')
    else:
        cf.read(configfile, encoding='utf-8')
    cf.remove_option(section,option)
    cf.set(section,option,values)
    cf.write(open(configfile,"w"))



if __name__ == '__main__':
    #os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    # print(setConfig("ceshi","region_single_pangu","cn-kunming-cmcc-2"))
    override_mapping={}
    if override_mapping:
        print(1)
    else:
        print(0)