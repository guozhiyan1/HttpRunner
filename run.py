from httprunner.api import HttpRunner
from httprunner.report.html import (gen_html_report)
from tools import DingTalk
from datetime import datetime
from httprunner.report import summarize
import sys

if __name__ == '__main__':
    args = sys.argv
    build_user_name = args[1]
    build_user_id = args[2]
    build_user_email = args[3]
    # runner = HttpRunner(failfast=False, log_level="debug")
    runner = HttpRunner(failfast=False, log_level="debug")
    # result = runner.run("testcase/hospital/HospitalizedRegister.yml", dot_env_path="test.env")
    result = runner.run("api/token.yml", dot_env_path="test.env")


    # 当前时间戳
    now_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # 生成报告
    gen_html_report(result, now_timestamp)
    # 钉钉通知
    DingTalk.DingTalkSend(now_timestamp, result)

    # 发送通知邮件



