from rest_framework import serializers
from goods.models import Goods,GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = '__all__'#('name', 'click_num', 'market_price', 'goods_front_image')
