import smtplib
from email.header import Header
from email.mime.text import MIMEText

from django.conf import settings

from . import settings


def send_email(email, mess):
    """
    发送邮件
    :param email: 发送到的邮箱号
    :param mess: 发送的信息
    :return:
    """
    msg = MIMEText('<html><div><p>{}</p></span></html>'.format(mess), "html", 'utf-8')
    msg["Subject"] = Header("邮箱验证码", "utf-8")
    msg["From"] = settings.USER
    msg['To'] = email

    smtp = smtplib.SMTP()
    smtp.connect(settings.HOST, settings.PORT)
    smtp.login(settings.USER, settings.PWD)
    smtp.sendmail(
        from_addr=msg["From"],
        to_addrs=msg["To"],
        msg=msg.as_string()
    )
