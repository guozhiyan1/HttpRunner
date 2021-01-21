from httprunner.api import HttpRunner
from httprunner.report.html import (gen_html_report)
from tools import report_data
from datetime import datetime
import sys
from tools import ding_talk, gmc_email


if __name__ == '__main__':
    args = sys.argv
    # build_user_name = args[1]
    # build_user_id = args[2]
    # build_user_email = args[3]
    #
    # runner = HttpRunner(failfast=False, log_level="debug")
    runner = HttpRunner(failfast=False, log_level="debug")
    # result = runner.run("testcase/hospital/add_bed.yml", dot_env_path="test.env")
    result = runner.run("testcase/smoking/cis/", dot_env_path="test.env")

    # 当前时间戳
    now_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # 生成报告
    gen_html_report(result, now_timestamp)

    # 生成通知内容
    result = report_data.generate_report(now_timestamp, result)

    # # 钉钉通知
    # ding_talk.DingTalkSend(result)
    #
    # # 发送通知邮件
    # emails = gmc_email.SendEmail(result)
    # emails.sendFile()


