from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import CreateUserSerializer


# Create your views here.
class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = CreateUserSerializer  # 指定序列化器


# class UserView1(GenericAPIView):
#     """用户注册"""
#     #指定序列化器
#     serializer_class = CreateUserSerializer
#     
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class UsernameCountView(APIView):
    """判断用户名是否已注册"""

    def get(self, request, username):
        # 查询user表
        count = User.objects.filter(username=username).count()
        # 包装相应数据
        data = {
            'username': username,
            'count': count
        }
        return Response(data)

class MobileCountView(APIView):
    """判断手机号是否已注册"""
    
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)
