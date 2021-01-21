from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # 注册
    path('users/', views.UserView.as_view()),
    # 判断用户名
    re_path(r'^users/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # JWT登录
    path('authorizations/', obtain_jwt_token),
]