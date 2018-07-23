import time
from random import Random
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.models import Goods
from goods.serializers import GoodsSerializer
from .models import ShopingCart, OrderInfo, OrderGoods


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)
    class Meta:
        model = ShopingCart
        fields = ("goods", "nums")


class ShopingCartSerializer(serializers.Serializer):
    '''
    购物车 ShopingCartSerializer
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(min_value=1,required=True,label='数量')
    goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        goods = validated_data['goods']
        num = validated_data['nums']
        shopCart = ShopingCart.objects.filter(user=user,goods=goods)
        if shopCart:
            shopCart = shopCart[0]
            shopCart.nums += num
            shopCart.save()
        else:
            shopCart = ShopingCart.objects.create(**validated_data)
        return shopCart

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance

class orderInfoSerializer(serializers.ModelSerializer):
    '''
       订单 orderInfoSerializer
       '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        # 当前时间+id+随机数
        random_ins = Random()
        order_sn = '{time_str}{userid}{ranstr}'.format(time_str= time.strftime('%Y%m%d%H%M%S'),userid=self.context['request'].user.id,ranstr=random_ins.randint(10,99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class orderGoodsSerializer(serializers.ModelSerializer):
    '''
    订单的商品详情 过滤类
    '''
    goods = GoodsSerializer(many=False)# goods 跟 Goods 建立联系

    class Meta:
        model = OrderGoods
        fields = "__all__"


class orderDetailSerializer(serializers.ModelSerializer):
    '''
    订单详情 过滤类
    '''
    goods = orderGoodsSerializer(many=True)# goods 跟OrderGoods建立联系

    class Meta:
        model = OrderInfo
        fields = "__all__"