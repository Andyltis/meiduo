import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """重写jwt登陆视图的构造相应数据函数， 多追加 user_id和username"""
    print(user.id, user.username)
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """
    通过传入的账号动态获取user模型对象
    :param account: 有可能是手机号， 有可能是用户名
    :return: user或None
    """
    try:
        if re.match(r'1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """修改Django的认证类， 为了实现多账号登陆"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取user
        user = get_user_by_account(username)
        # 判断当前前端传入的密码是否正确
        if user and user.check_password(password):
            # 返回user
            return user

