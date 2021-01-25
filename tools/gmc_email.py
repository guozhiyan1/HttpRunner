import smtplib
from email.mime.text import MIMEText
from config import config
from email.header import Header
from smtplib import SMTP_SSL


class SendEmail(object):
    """
    发送邮件模块
    """

    def __init__(self, result):
        self.mail_smtpserver = config.get_conf("Email", "mail_smtpserver")
        self.mail_port = config.get_conf("Email", "mail_port")
        self.mail_sender = config.get_conf("Email", "mail_sender")
        self.mail_pwd = config.get_conf("Email", "mail_pwd")
        # 接收邮件列表
        self.mail_receiverList = ["xuxiaojing@come-future.com"]
        self.result = result

    def sendFile(self):
        """
        发送各种类型的附件
        """

        mail_content = f"""<p>您好，您的自动化测试任务已完成，以下是测试结果请查收: </p>
                       <p><a href = "{self.result['url']}" >点击查看测试报告 </a></p>
                       <a href = "{self.result['jenkins_url']}" >点击查看jenkins构建地址 </a>
                       <p>测试结果：<font size="2" color={'green' if self.result['flag'] else 'red'}>{self.result['result']}</font></p>
                       <p>通过用例：<font size="2" color="green">{self.result['pass']}</font> </p> 
                       <p>失败用例：<font size="2" color="red">{self.result['fail']}</font></p> 
                       <p>跳过用例：<font size="2" color="grey">{self.result['skip']}</font> </p>"""

        # 邮件标题
        mail_title = '自动化测试邮件'

        msg = MIMEText(mail_content, "html", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = self.mail_sender
        msg["To"] = Header("可乐", 'utf-8')  ## 接收者的别名

        smtp = SMTP_SSL(self.mail_smtpserver)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        # smtp.set_debuglevel(1)
        smtp.ehlo(self.mail_smtpserver)
        smtp.login(self.mail_sender, self.mail_pwd)

        # 函数：sendmail(self, from_addr, to_addrs, msg, mail_options=[],rcpt_options=[]):
        smtp.sendmail(self.mail_sender, self.mail_receiverList, msg.as_string())
        smtp.quit()




# 调试
if __name__ == "__main__":
    results = {'url': 'http://localhost:63342/gmc-http-test-master/reports/20210113171718.html', 'result': '测试通过', 'jenkins_url': 'http://jenkins-gmc-dev.cfuture.shop/', 'pass': '1', 'fail': '0', 'skip': '0'}
    s = SendEmail(results)
    s.sendFile()
