from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from .models import UserFav,UserLeavingMessage,UserAddress
from django.contrib.auth import get_user_model
User = get_user_model()


class userFavDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情 userFavDetailSerializer
    '''
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class userFavSerializer(serializers.ModelSerializer):
    '''
    用户收藏 过滤 userFavSerializer
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]
        model = UserFav
        fields = ('user','goods','id')


class userLeavingSerializer(serializers.ModelSerializer):
    '''
    用户留言 userLeavingSerializer
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'id','message_type','subject','message','file','add_time')


class userAddressSerializer(serializers.ModelSerializer):
    '''
    用户地址 userAddressSerializer
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserAddress
        fields = ('user', 'id', 'district','province','city', 'address', 'signer_name', 'signer_mobile')
