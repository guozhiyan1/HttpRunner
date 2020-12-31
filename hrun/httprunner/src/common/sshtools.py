#!/usr/bin/env python
# -*- coding: utf-8 -*-
# paramiko

import time
import paramiko
from loguru import logger


class ApiTest(object):
    # ssh连接基本参数
    def __init__(self, ip, password, user="root"):
        self.ip = ip
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.user = user

    def ssh_connect(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for i in range(100):
            time.sleep(10)
            try:
                self.ssh.connect(self.ip, 22, self.user, self.password)
                logger.info(f"{self.ip} : 连接成功")
                break
            except Exception as e:
                logger.debug(f"{self.ip}: 连接失败 {e}")

    def ssh_exec_command(self, command):
        """
        执行指定命令
        结果放到stdout中，如果有错误将放到stderr中
        :return: stdout, stderr
        """
        stdin, stdout, stderr = self.ssh.exec_command(command)
        # 标准输出解码
        stdout = self.stdout_decode(stdout)
        stderr = self.stdout_decode(stderr)

        # 判断命令是否运行成功
        if stderr:
            logger.debug(f"{command} \n命令执行异常:  {stderr}")
        else:
            logger.info(f"{command} 命令执行成功")
        # 'sudo sysbench --test=cpu --cpu-max-prime=500000 --threads=32 run'
        return stdout, stderr

    def stdout_decode(self, stdout):
        """
        标准输出解码
        :param stdout:
        :return:
        """
        return str(stdout.read().decode('utf-8'))

    def ssh_instance_network(self, ip2=None):
        """
        用ping命令检查网络
        :param ip2: 内网ip
        :return:
        """
        flag = True
        stdout_list = dict()
        stdout_list[self.ip] = self.ssh_exec_command('ping -c 2 www.baidu.com;ping -c 2 %s' % self.ip)
        if ip2:
            stdout_list[ip2] = self.ssh_exec_command('ping -c 2 %s' % ip2)
        for i in stdout_list:
            if self.ssh_ping(stdout_list[i][0]):
                logger.info(f"{i}:ping success")
            else:
                flag = False
        return flag

    def ssh_ping(self, stdout):
        """
        检验ping丢包率
        :param stdout:
        :return: 是否ping成功
        """
        return True if stdout.find('0% packet') > 0 else False

    def ssh_instance_disk(self, dev="/dev/vdb"):
        """
        磁盘分区、格式化、挂载、读写
        :param dev:
        :return:
        """
        stdout, stderr = self.ssh_exec_command(f'''
                  echo "n
                  p



                  w" | fdisk {dev} &&mkfs.ext4 {dev+"1"}
                  sleep 5
                  mkdir test
                  mount {dev+"1"} test
                  echo 'test1 success' > test/cabc.txt
                  sleep 1
                  cat test/cabc.txt
                  df -h
                  ''')
        return True if stdout.find('test1 success') and stdout.find(dev+"1") else False

    def ssh_close(self):
        return self.ssh.close()


# 调用请求
if __name__ == '__main__':
    a = ApiTest('180.97.159.133', "a123456789*")
    # a.ssh_connect()
    # print(a.ssh_instance_disk())
    # print(a.ssh_instance_network('10.0.7.9922'))
