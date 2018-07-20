from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from .models import UserFav
from django.contrib.auth import get_user_model
User = get_user_model()


class userFavDetailSerializer(serializers.ModelSerializer):
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
