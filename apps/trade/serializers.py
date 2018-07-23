import time
from random import Random
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from RXYshop.settings import private_key_path, ali_pub_key_path, ALI_PAY_APPID
from goods.models import Goods
from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
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
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,obj):
        alipay = AliPay(
            appid=ALI_PAY_APPID,
            app_notify_url="http://39.106.22.205:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://39.106.22.205:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,  # "2017020212223",
            total_amount=obj.order_mount,
            return_url="http://39.106.22.205:8000/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

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
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=ALI_PAY_APPID,
            app_notify_url="http://39.106.22.205:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://39.106.22.205:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,  # "2017020212223",
            total_amount=obj.order_mount,
            return_url="http://39.106.22.205:8000/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"