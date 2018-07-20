"""RXYshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from DjangoUeditor.views import get_ueditor_controller
from RXYshop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import xadmin,DjangoUeditor

from goods.views import GoodsListViewSet,GoodsCategoryListViewSet
from user_operation.views import userFavViewSet
from users.views import SmsCoeViewSet,userRegViewSet

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet,base_name='goods')
# GoodsCategoryListViewSet
router.register(r'category', GoodsCategoryListViewSet,base_name='category')
# 配置发送短信SmsCoeViewSet的url
router.register(r'sendSms', SmsCoeViewSet,base_name='sendSms')
# 配置注册 userRegViewSet 的url
router.register(r'register', userRegViewSet,base_name='register')
# 配置收藏功能 userFavViewSet 的url
router.register(r'userfavs', userFavViewSet,base_name='userfavs')


urlpatterns = [
    url(r'^xadmin/',xadmin.site.urls),

    url(r'^ueditor/controller/$', get_ueditor_controller),

    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),

    url(r'^', include(router.urls)),
    #url(r'goods/$',goods_list,name='goods-list'),
    url(r'docs/',include_docs_urls(title="融鑫源API")),
    # drf 自带的token模式
    #url(r'^api-token-auth/', views.obtain_auth_token)
    # jwt认证接口
    url(r'^login/', obtain_jwt_token),

]
