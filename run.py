from httprunner.api import HttpRunner
from httprunner.report.html import (gen_html_report)
from tools import DingTalk
import datetime

if __name__ == '__main__':
    # runner = HttpRunner(failfast=False, log_level="debug")

    runner = HttpRunner(failfast=False, log_level="debug")

    # result = runner.run("testcase/hospital/HospitalizedRegister.yml", dot_env_path="test.env")
    # result = runner.run("testcase/hospital/queryHospitalizedRegister.yml", dot_env_path="test.env")
    result = runner.run("api/token.yml", dot_env_path=".env")


    now_timestamp = datetime.now().strftime('%Y%m%d %H%M%S')
    # 生成报告
    gen_html_report(result, now_timestamp)

    DingTalk.DingTalkSend(now_timestamp)

