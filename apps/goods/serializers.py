from rest_framework import serializers
from django.db.models import Q
from .models import Goods,GoodsCategory,GoodsImage,HotSearchWords,Banner,GoodsCategoryBrand,IndexAd


class CategorySerializer3(serializers.ModelSerializer):
    '''
   商品3级分类（提交数据过滤 、 返回数据显示过滤）
   '''
    class Meta:
        model = GoodsCategory
        fields = '__all__'  # ('name', 'click_num', 'market_price', 'goods_front_image')


class CategorySerializer2(serializers.ModelSerializer):
    '''
   商品2级分类（提交数据过滤 、 返回数据显示过滤）
   '''
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')


class CategorySerializer(serializers.ModelSerializer):
    '''
    商品1级分类（提交数据过滤 、 返回数据显示过滤）
    '''
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')


class GoodsImageSerializer(serializers.ModelSerializer):
    '''
    商品轮播图（提交数据过滤 、 返回数据显示过滤）
    '''
    class Meta:
        model = GoodsImage
        fields = ('image',)#('name', 'click_num', 'market_price', 'goods_front_image')


class GoodsSerializer(serializers.ModelSerializer):
    '''
    商品（提交数据过滤 、 返回数据显示过滤）
    '''
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')


class HotSearchWordsSerializer(serializers.ModelSerializer):
    '''
    热搜词 serializer（提交数据过滤 、 返回数据显示过滤）
    '''
    class Meta:
        model = HotSearchWords
        fields = ('keywords',)  # ('name', 'click_num', 'market_price', 'goods_front_image')


class BannersSerializer(serializers.ModelSerializer):
    '''
    热搜词 serializer（提交数据过滤 、 返回数据显示过滤）
    '''
    class Meta:
        model = Banner
        fields = '__all__'  # ('name', 'click_num', 'market_price', 'goods_front_image')


class BrandSerializer(serializers.ModelSerializer):
    '''
    品牌 serializer（提交数据过滤 、 返回数据显示过滤）
    '''
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    '''
    首页商品分类数据显示 serializer（提交数据过滤 、 返回数据显示过滤）
    '''
    brands = BrandSerializer(many=True)
    sub_cat = CategorySerializer2(many=True)
    goods = serializers.SerializerMethodField()
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self,obj):
        goods =Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    def get_ad_goods(self, obj):
        ad_goods_json = {}
        indexAds = IndexAd.objects.filter(category_id=obj.id,)
        if indexAds:
            goods_ins = indexAds[0].goods
            ad_goods_json = GoodsSerializer(goods_ins, many=False, context={'request': self.context['request']})
        return ad_goods_json.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
