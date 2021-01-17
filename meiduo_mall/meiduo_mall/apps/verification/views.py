from django.shortcuts import render
from rest_framework.views import APIView
from random import randint
from django_redis import get_redis_connection
from meiduo_mall.libs.yuntongxun.sms import CCP
from rest_framework.response import Response
# Create your views here.
class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1.生成验证码
        sms_code = "%06d" % randint(0, 999999)
        # 2.创建redis连接对象
        redis_conn = get_redis_connection("verify_codes")
        # 3.把验证码储存到redis数据库
        redis_conn.setex("sms_%s" % mobile, 300, sms_code)  # 300过期时间
        # 4.利用荣联运通讯发送短信验证码
        # CCP().send_template_sms("手机号", [验证码, 5], 1)  # 5过期时间 1 模板选择
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 5.响应
        return Response({"message": "ok"})
        pass
