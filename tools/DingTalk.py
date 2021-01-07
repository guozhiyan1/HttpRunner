import os
# 安装pip install python-jenkins
import jenkins
import json
import urllib3
import platform
from config import config

# jenkins登录地址
jenkins_url = config.get_conf("jenkins", "jenkins_url")
# 获取jenkins对象
# Jenkins登录名 ，密码
username = config.get_conf("jenkins", "username")
password = config.get_conf("jenkins", "password")
server = jenkins.Jenkins(jenkins_url, username=username, password=password)
# job名称
# Jenkins运行任务名称
job_name = config.get_conf("jenkins", "job_name")
# job的url地址
job_url = jenkins_url + job_name
# 获取最后一次构建
job_last_build_url = server.get_info(job_name)['lastBuild']['url']

'''
钉钉推送方法：
读取report文件中"prometheusData.txt"，循环遍历获取需要的值。
使用钉钉机器人的接口，拼接后推送text
'''


def DingTalkSend(now_timestamp):
    # 报告地址
    # report_url = job_last_build_url + 'HTML_20Report' #'allure'为我的Jenkins全局工具配置中allure别名
    remote_ip = config.get_conf("remote", "remote_ip")
    remote_report_url = 'http://' + remote_ip + '/gmc-http-autotest/reports/' + now_timestamp + '.html'
    local_report_url = 'http://localhost:63344/gmc-http-test/reports/' + now_timestamp + '.html'
    # 获取项目绝对路径
    path = os.path.abspath(os.path.dirname((__file__)))
    # 打开prometheusData 获取需要发送的信息
    # 　f = open(path + r'/allure-report/export/prometheusData.txt', 'r')
    # for lines in f:
    #     for _ in lines:
    #         launch_name = lines.strip('\n').split(' ')[0]
    #         num = lines.strip('\n').split(' ')[1]
    #         d.update({launch_name: num})
    # print(d)
    # f.close()
    # retries_run = d.get('launch_retries_run')  # 运行总数
    # print('运行总数:{}'.format(retries_run))
    # status_passed = d.get('launch_status_passed')  # 通过数量
    # print('通过数量：{}'.format(status_passed))
    # status_failed = d.get('launch_status_failed')  # 不通过数量
    # print('通过数量：{}'.format(status_failed))

    # 钉钉推送
    url = config.get_conf("dingding", "dingtalk_url")
    # windows和mac为本地路径
    flag = platform.system() == 'Windows' or platform.system() == 'Darwin'
    con = {"msgtype": "text",
           "text": {
               "content": "Pytest_Allure_Demo自动化脚本执行完成"
                          "\n测试概述:"
                          # "\n运行总数:" + retries_run +
                          # "\n通过数量:" + status_passed +
                          # "\n失败数量:" + status_failed +
                          "\n构建地址：\n" + job_url +
                          "\n报告地址：\n" + (remote_report_url if (flag == True) else local_report_url)
           }
           }
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    jd = json.dumps(con)
    jd = bytes(jd, 'utf-8')
    print(">>>>>>>>>>>>>>>>>", url, jd)
    http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    DingTalkSend()
