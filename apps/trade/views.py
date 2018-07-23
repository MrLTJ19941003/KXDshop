from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin,ListModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopingCartSerializer,ShopCartDetailSerializer,orderInfoSerializer,orderDetailSerializer
from .models import ShopingCart, OrderInfo, OrderGoods
from RXYshop.settings import ALI_PAY_APPID,private_key_path,ali_pub_key_path
from datetime import datetime

class ShopingCartViewSet(viewsets.ModelViewSet):
    '''
    购物车管理
     list:
        获取购物车列表
     create：
        新增购物记录
     destroy：
        删除购物记录
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class =ShopingCartSerializer
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopingCartSerializer

    def get_queryset(self):
        return ShopingCart.objects.filter(user=self.request.user)


class OrderInfoViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,CreateModelMixin,viewsets.GenericViewSet):
    '''
       订单管理
        list:
           获取订单列表
        create：
           新增订单记录
        destroy：
           删除订单记录
        retrieve:
           获取订单详情
       '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = orderInfoSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return orderDetailSerializer
        else:
            return orderInfoSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shopCarts = ShopingCart.objects.filter(user=self.request.user)
        for shopCart in shopCarts:
            # 向订单的商品详情中添加当前订单的商品信息
            order_goods = OrderGoods()
            order_goods.goods = shopCart.goods
            order_goods.goods_num = shopCart.nums
            order_goods.order = order
            order_goods.save()
            # 删除购物车商品
            shopCart.delete()

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect

class alipayViewSet(APIView):
    '''
    处理支付宝返回结果接口
    '''
    def get(self,request):
        '''
        处理支付宝 return_url 请求
        :param request:
        :return:
        '''
        proessed_dict = {}
        for key, value in request.GET.items():
            proessed_dict[key] = value
        sign = proessed_dict.pop('sign', None)

        alipay = AliPay(
            appid=ALI_PAY_APPID,
            app_notify_url="http://39.106.22.205:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://39.106.22.205:8000/alipay/return/"
        )

        verify_re = alipay.verify(proessed_dict, sign)
        if verify_re is True:
            order_sn = proessed_dict.get('out_trade_no', None)
            trade_no = proessed_dict.get('trade_no', None)
            trade_status = proessed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                if existed_order.pay_status == 'TRADE_SUCCESS':
                    continue
                else:
                    existed_order.trade_no = trade_no
                    existed_order.pay_status = trade_status
                    existed_order.pay_time = datetime.now()
                    existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response
            # return Response('success')

    def post(self,request):
        '''
        处理支付宝 notify_url 请求
        :param request:
        :return:
        '''
        proessed_dict = {}
        for key , value in request.POST.items():
            proessed_dict[key]=value
        sign = proessed_dict.pop('sign',None)

        alipay = AliPay(
            appid=ALI_PAY_APPID,
            app_notify_url="http://39.106.22.205:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://39.106.22.205:8000/alipay/return/"
        )

        verify_re = alipay.verify(proessed_dict,sign)
        if verify_re is True:
            order_sn = proessed_dict.get('out_trade_no',None)
            trade_no = proessed_dict.get('trade_no', None)
            trade_status = proessed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                if existed_order.pay_status == 'TRADE_SUCCESS':
                    continue
                else:
                    existed_order.trade_no = trade_no
                    existed_order.pay_status = trade_status
                    existed_order.pay_time = datetime.now()
                    existed_order.save()

            return Response('success')
