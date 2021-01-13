import os
import json
import urllib3
import platform
from config import config
import sys

"""
# username = config.get_conf("jenkins", "username")
# password = config.get_conf("jenkins", "password")
# server = jenkins.Jenkins(jenkins_url, username=username, password=password)
# job_last_build_url = server.get_info(job_name)['lastBuild']['url']

"""

jenkins_url = config.get_conf("jenkins", "jenkins_url")
job_name = config.get_conf("jenkins", "job_name")
job_url = jenkins_url + job_name


def generate_report(now_timestamp, result):
    remote_ip = config.get_conf("remote", "remote_ip")
    project_name = os.path.split(sys.path[1])[1]
    visit_url = project_name + '/reports/' + now_timestamp + '.html'
    remote_report_url = 'http://' + remote_ip + '/' + visit_url
    local_report_url = 'http://localhost:' + config.get_conf("local",
                                                              "html_open_port") + '/' + visit_url
    flag = platform.system() == 'Windows' or platform.system() == 'Darwin'

    result = {"url": local_report_url if flag else remote_report_url,
              "result": f"{'测试通过'  if result['success'] else '测试不通过'}",
              "jenkins_url": f"{jenkins_url}",
              "pass": f"{result['stat']['teststeps']['successes']}",
              "fail": f"{result['stat']['teststeps']['failures']}",
              "skip": f"{result['stat']['teststeps']['skipped']}"}

    return result

