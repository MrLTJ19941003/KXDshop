from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin,ListModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopingCartSerializer,ShopCartDetailSerializer,orderInfoSerializer
from .models import ShopingCart,OrderInfo


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

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)