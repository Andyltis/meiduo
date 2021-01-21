import re

from django_redis import get_redis_connection
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    # 序列化器的所有字段： 【'id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow'】
    # 需要校验的字段： 【'username', 'password', 'password2', 'mobile', 'sms_code', 'allow'】
    # 模型中已存在的字段： 【'username', 'password','mobile'】

    # 需要序列化的字段【‘id’, 'username', 'mobile'】
    # 需要反序列化字段【'username', 'password', 'password2', 'mobile', 'sms_code', 'allow'】

    # read_only 只序列化  write_only  只反序列化
    password2 = serializers.CharField(label="确认密码", write_only=True)
    sms_code = serializers.CharField(label="验证码", write_only=True)
    allow = serializers.CharField(label="同意协议", write_only=True)  # 'true'

    class Meta:
        model = User  # 从user模型中映射序列化器字段
        # fields = '__all__'
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的⽤用户名',
                    'max_length': '仅允许5-20个字符的⽤用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式有误")

        return value

    def validate_allow(self, value):
        """是否同意协议校验"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, attrs):
        """校验密码是否正确"""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("两个密码不一致")
        # 校验密码
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get("sms_%s" % attrs['mobile'])
        # 向redis储存数据都是以字符串进行储存的， 取出来后都是bytes类型

        if real_sms_code is None:
            raise serializers.ValidationError("无效的验证码")
        if attrs["sms_code"] != real_sms_code.decode():
            raise serializers.ValidationError("验证码错误")

        return attrs

    def create(self, validated_data):
        # 把不需要存储的字段从字典中移除
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)  # 把密码加密后再赋值给user的password属性
        user.save()  # 储存到数据库

        return user
