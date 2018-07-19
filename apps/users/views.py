# Create your views here.
from random import choice

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler,jwt_encode_handler

from .serializers import SmsSerializer,userRegSerializer
from utils.yunpian import YunPian
from RXYshop.settings import API_KEY
from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCoeViewSet(CreateModelMixin,viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsSerializer

    def generateCode(self):
        '''
        生成四位数的验证码
        :return:
        '''
        seeds = "1234567890"
        random_str = []
        for r in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)


    def create(self, request, *args, **kwargs):
        '''
        验证手机号码并发送验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yunpian = YunPian(API_KEY)
        code = self.generateCode()
        sms_status = yunpian.send_Sms(code=code,mobile=mobile)
        if sms_status['code'] != 0:
            return Response({
                "mobile":sms_status['msg']
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            verifyCode = VerifyCode(mobile=mobile,code=code)
            verifyCode.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

class userRegViewSet(CreateModelMixin,viewsets.GenericViewSet):
    '''
    用户注册 viewSet
    '''
    serializer_class = userRegSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
