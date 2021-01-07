import os
# 安装pip install python-jenkins
import jenkins
import json
import urllib3
import platform
from config import config
import sys

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


def DingTalkSend(now_timestamp, result):
    remote_ip = config.get_conf("remote", "remote_ip")
    project_name = os.path.split(sys.path[1])[1]
    visit_url = project_name + '/reports/' + now_timestamp + '.html'
    remote_report_url = 'http://' + remote_ip + '/' + visit_url
    local_report_url = 'http://localhost:' + config.get_conf("local",
                                                              "html_open_port") + '/' + visit_url
    # 获取项目绝对路径
    # path = os.path.abspath(os.path.dirname((__file__)))
    # 钉钉推送
    url = config.get_conf("dingding", "dingtalk_url")
    # windows和mac为本地环境
    flag = platform.system() == 'Windows' or platform.system() == 'Darwin'

    context = {
     "msgtype": "markdown",
     "markdown": {
         "title": "[gmc-http-test]自动化测试",
         "text": f"### gmc-http-test自动化测试结果\n>####  [查看测试报告]({local_report_url if flag else remote_report_url}) \n>####  [查看构建地址]({job_url}) \n"
                 f"#### 测试结果：{'测试通过'  if result['success'] else '测试不通过'}\n"
                 f"#### 通过用例：{result['stat']['teststeps']['successes']}\n"
                 f"#### 失败用例：{result['stat']['teststeps']['failures']}\n"
                 f"#### 跳过用例：{result['stat']['teststeps']['skipped']}\n"
     },
     "at": {
          "atMobiles": [
              "15757115799"
          ],
          "isAtAll": False
      }
    }
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    jd = json.dumps(context)
    jd = bytes(jd, 'utf-8')
    print(">>>>>>>>>>>>>>>>>", url, jd)
    http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})
