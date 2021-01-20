# 必须 tasks.py
from celery_tasks.main import celery_app
from celery_tasks.sms.send_email import send_email


@celery_app.task(name="send_sms_code")
def send_sms_code(email="22814852@qq.com", sms_code='000000'):
    """
    发送邮件的异步任务
    :param email:
    :param sms_code:
    :return:
    """
    send_email(email, "验证码： {}".format(sms_code))
