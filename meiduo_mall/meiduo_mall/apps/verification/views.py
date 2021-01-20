from django.shortcuts import render
from rest_framework.views import APIView
from random import randint
from django_redis import get_redis_connection
from meiduo_mall.libs.yuntongxun.sms import CCP
from meiduo_mall.libs.send_email import send_email
from rest_framework.response import Response
from rest_framework import status
from  . import constants


# Create your views here.
class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1.创建redis连接对象
        redis_conn = get_redis_connection("verify_codes")
        # 2.先从redis获取发送标记
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:  # 此手机号已发送短信
            return Response({"message": '手机频繁发送短信'}, status=status.HTTP_400_BAD_REQUEST)

        # 3.生成验证码
        sms_code = "%06d" % randint(0, 999999)
        print(sms_code)

        # 4.把验证码储存到redis数据库
        redis_conn.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)  # 300过期时间
        # 4.1 储存一个标记，表示此手机号已发送短信， 标记有效期60s
        redis_conn.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 5.利用荣联运通讯发送短信验证码
        # CCP().send_template_sms("手机号", [验证码, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)  # 5过期时间 1 模板选择
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        send_email("22814852@qq.com", "验证码： {}".format(sms_code))
        # 6.响应
        return Response({"message": "ok"})
        pass
