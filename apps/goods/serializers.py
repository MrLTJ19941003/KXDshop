from rest_framework import serializers
from goods.models import Goods,GoodsCategory,GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'  # ('name', 'click_num', 'market_price', 'goods_front_image')


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)#('name', 'click_num', 'market_price', 'goods_front_image')


class GoodsSerializer(serializers.ModelSerializer):
    '''
    商品过滤类
    '''
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')
