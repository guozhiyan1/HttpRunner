import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


class SendEmail(object):
    '''
    发送邮件模块封装，属性均从config.ini文件获得
    '''

    def __init__(self, smtpServer, mailPort, mailSender, mailPwd, mailtoList, mailSubject):
        self.mail_smtpserver = smtpServer
        self.mail_port = mailPort
        self.mail_sender = mailSender
        self.mail_pwd = mailPwd
        # 接收邮件列表
        self.mail_receiverList = mailtoList
        self.mail_subject = mailSubject
        # self.mail_content = mailContent

    def sendFile(self):
        '''
        发送各种类型的附件
        '''
        # 构建根容器
        msg = MIMEMultipart()

        # 邮件正文部分body，1、可以用HTML自己自定义body内容；2、读取其他文件的内容为body
        # body = "您好，<p>这里是使用Python登录邮箱，并发送附件的测试<\p>"
        # with open(reportFile, 'r', encoding='UTF-8') as f:
        #     body = f.read()

        # _charset 是指Content_type的类型
        msg.attach(MIMEText(_text="222", _subtype='html', _charset='utf-8'))

        # 邮件主题、发送人、收件人、内容
        msg['Subject'] = self.mail_subject  # u'自动化测试报告'
        msg['from'] = self.mail_sender
        msg['to'] = self.mail_pwd

        # # 添加附件
        # attachment = MIMEText(_text=open(reportFile, 'rb').read(), _subtype='base64', _charset='utf-8')
        # attachment['Content-Type'] = 'application/octet-stream'
        # attachment['Content-Disposition'] = 'attachment;filename = "result.html"'
        # msg.attach(attachment)
        #
        # try:
        #     smtp = smtplib.SMTP_SSL(host=self.mail_smtpserver, port=self.mail_port)  # 继承自SMTP
        # except:
        smtp = smtplib.SMTP()
        smtp.connect(self.mail_smtpserver, self.mail_port)

        # smtp.set_debuglevel(1)
        # 创建安全连接，加密SMTP
        smtp.starttls()  # Puts the connection to the SMTP server into TLS mode.
        # 用户名和密码
        smtp.login(user=self.mail_sender, password=self.mail_pwd)

        # 函数：sendmail(self, from_addr, to_addrs, msg, mail_options=[],rcpt_options=[]):
        smtp.sendmail(self.mail_sender, self.mail_receiverList, msg.as_string())
        smtp.quit()


# 调试代码
if __name__ == "__main__":
    mail_smtpserver = 'smtp.exmail.qq.com'
    mail_port = 587
    mail_sender = 'cops@come-future.com'
    mail_pwd = 'bv7T9yzrYpCyKFt5'
    mail_receiverList = ['xuxiaojing@come-future.com']
    mail_subject = u'自动化测试报告'
    s = SendEmail(mail_smtpserver, mail_port, mail_sender, mail_pwd, mail_receiverList, mail_subject)
    s.sendFile()
