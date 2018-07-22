from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin,ListModelMixin,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .models import UserFav,UserLeavingMessage,UserAddress
from .serializers import userFavSerializer, userFavDetailSerializer,userLeavingSerializer,userAddressSerializer


class userFavViewSet(CreateModelMixin,ListModelMixin,DestroyModelMixin,RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    '''
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        '''
        动态调用返回的Serializer
        :return:
        '''
        if self.action == "list":
            return userFavDetailSerializer
        elif self.action == "create":
            return userFavSerializer
        return userFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class LeavingViewSet(CreateModelMixin,DestroyModelMixin,ListModelMixin,viewsets.GenericViewSet):
    '''
     list:
        获取用户留言列表
    destroy:
        删除用户留言
    create:
        新建用户留言
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = userLeavingSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

class AddressViewSet(CreateModelMixin,UpdateModelMixin,DestroyModelMixin,ListModelMixin,viewsets.GenericViewSet):
    '''
        list:
           获取用户收货地址列表
       destroy:
           删除用户收货地址
       create:
           新建用户收货地址
        patch:
            更新用户收货地址
       '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = userAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)