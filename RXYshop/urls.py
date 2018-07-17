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
# from django.contrib import admin
from django.conf.urls import url, include
import xadmin
from RXYshop.settings import MEDIA_ROOT
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from goods.views import GoodsListView

urlpatterns = [
    url(r'^xadmin/',xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),

    url(r'goods/$',GoodsListView.as_view(),name='goods-list'),
    url(r'doc/',include_docs_urls(title="融鑫源")),


]
