from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(email, mess):
    """
    发送邮件
    :param email: 发送到的邮箱号
    :param mess: 发送的信息
    :return:
    """
    subject = "登陆验证码"
    text_content = '''123'''

    html_content = '<p>{}</p>'.format(mess)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
