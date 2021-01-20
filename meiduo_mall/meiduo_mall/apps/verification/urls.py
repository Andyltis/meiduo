from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('<int: mobile>'),
    re_path(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
    # re_path(r'^sms_code/(?P<mobile>.*?@.*?\.com)/$', views.SMSCodeView.as_view())
]