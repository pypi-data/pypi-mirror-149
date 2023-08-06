import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


# 邮件通知
from qrunner.utils.allure_data import AllureData


class Mail:
    def __init__(self, host, user, password):
        self.host = host
        self.username = user
        self.password = password

    def send_mail(self, mail_data, receivers):
        print(f'向{receivers}发送邮件...')
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header(self.username)
        message['To'] = Header(",".join(receivers))
        message['Subject'] = Header(mail_data.get('title'), 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText(mail_data.get('body'), 'plain', 'utf-8'))
        # 附件
        file_path = mail_data.get('file_path')
        if file_path:
            # 构造附件，传送当前目录下的文件
            att1 = MIMEText(open(file_path, 'r').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            file_name = mail_data.get('file_name')
            att1["Content-Disposition"] = f'attachment; filename="{file_name}"'
            message.attach(att1)

        # 连接
        conn = smtplib.SMTP_SSL(self.host, 465)
        # 登录
        conn.login(self.username, self.password)
        # 发送邮件
        try:
            conn.sendmail(self.username, receivers, message.as_string())
        except Exception as e:
            print(f'发送失败: {str(e)}')
        else:
            print('发送成功')
        # 断开连接
        conn.quit()

    def send_report(self, title, report_url, receiver_list):
        allure_data = AllureData.get_basic_info('report')
        total = allure_data.get('total')
        fail = allure_data.get('fail')
        passed = allure_data.get('passed')
        rate = allure_data.get('rate')
        body_str = '\n\n\t共 {0} 个用例，通过 {1} 个，失败 {2} 个，通过率 {3}%，详见: {4}'.format(total, passed, fail, rate, report_url)

        # 邮件内容
        msg_data = {
            'title': title,
            'body': body_str,
            'file_path': None,
            'file_name': None
        }

        self.send_mail(msg_data, receiver_list)


if __name__ == '__main__':
    host = 'smtphm.qiye.163.com'
    user = 'kang.yang@qizhidao.com'
    pwd = 'Yang1990315'
    # 收件人
    receiver_list = ['kang.yang@qizhidao.com']
    mail = Mail(host, user, pwd)
    mail.send_report('测试邮件标题', '111', receiver_list)



