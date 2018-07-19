import re
from datetime import datetime,timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from RXYshop.settings import REGEX_MOBILE
from .models import VerifyCode
from django.contrib.auth import get_user_model
User = get_user_model()


class SmsSerializer(serializers.Serializer):
    '''
    发送短信 过滤
    '''
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param attrs:
        :return:
        '''
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_age = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_age,mobile=mobile).count():
            raise serializers.ValidationError("距离发送未超过60s")

        return mobile


class userRegSerializer(serializers.ModelSerializer):
    '''
    用户注册过滤
    '''
    code = serializers.CharField(label="验证码",write_only=True,max_length=4,min_length=4,required=True)
    username = serializers.CharField(label="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type':'password'},
        label="密码",
        write_only=True
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_records = verify_records[0]
            five_mintes_age = datetime.now() - timedelta(hours=0, minutes=50, seconds=0)
            if five_mintes_age > last_records.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_records.code != code:
                raise serializers.ValidationError("验证码过期")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs["code"]
        print(attrs)
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile","password")
