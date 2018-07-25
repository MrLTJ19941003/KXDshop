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

from goods.views import GoodsListViewSet,GoodsCategoryListViewSet,HotSearchWordsViewSet,BannersViewSet,IndexgoodsViewSet
from user_operation.views import userFavViewSet,LeavingViewSet,AddressViewSet
from users.views import SmsCoeViewSet,userRegViewSet
from trade.views import ShopingCartViewSet,OrderInfoViewSet,alipayViewSet

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

# 配置留言功能 LeavingViewSet 的url
router.register(r'messages', LeavingViewSet,base_name='messages')

# 配置用户收货地址功能 AddressViewSet 的url
router.register(r'address', AddressViewSet,base_name='address')

# 配置购物车功能 ShopingCartViewSet 的url
router.register(r'shopcarts', ShopingCartViewSet,base_name='shopcarts')

# 配置订单管理功能 OrderInfoViewSet 的url
router.register(r'orders', OrderInfoViewSet,base_name='orders')

# 配置热搜词查询功能 HotSearchWordsViewSet 的url
router.register(r'hotsearchs', HotSearchWordsViewSet,base_name='hotsearchs')

# 配置轮播图查询功能 bannersViewSet 的url
router.register(r'banners', BannersViewSet,base_name='banners')

# 配置首页商品分类查询功能 IndexgoodsViewSet 的url
router.register(r'indexgoods', IndexgoodsViewSet,base_name='indexgoods')

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^xadmin/',xadmin.site.urls),

    url(r'^ueditor/controller/$', get_ueditor_controller),

    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),

    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),

    url(r'^', include(router.urls)),

    #url(r'goods/$',goods_list,name='goods-list'),
    url(r'docs/',include_docs_urls(title="融鑫源API")),
    # drf 自带的token模式
    #url(r'^api-token-auth/', views.obtain_auth_token)
    # jwt认证接口
    url(r'^login/', obtain_jwt_token),

    # 支付宝支付接收接口
    url(r'^alipay/return/', alipayViewSet.as_view(),name="alipay"),

]
