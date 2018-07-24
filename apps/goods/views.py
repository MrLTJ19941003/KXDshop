# Create your views here.

from rest_framework import mixins,filters,viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Goods,GoodsCategory,HotSearchWords,Banner
from .filters import GoodsFilter
from .serializers import GoodsSerializer,CategorySerializer,HotSearchWordsSerializer,BannersSerializer,IndexCategorySerializer


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    通过rest_framework的view实现商品列表页 分页、搜索、过滤、排序
    """
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    queryset = Goods.objects.all()
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name','goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    通过rest_framework的view实现商品类别查询
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchWordsViewSet(CacheResponseMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    热搜词查询
    '''
    queryset = HotSearchWords.objects.all().order_by('-index')
    serializer_class = HotSearchWordsSerializer


class BannersViewSet(CacheResponseMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    首页轮播图查询查询
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannersSerializer


class IndexgoodsViewSet(CacheResponseMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    首页商品分类数据显示
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer

