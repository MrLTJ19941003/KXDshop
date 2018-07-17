# -*- coding: utf-8 -*-
__author__ = 'liutj'

# 独立使用Django的model
import sys,os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RXYshop.settings")

import django
django.setup()

from db_tools.data.product_data import row_data
from goods.models import Goods,GoodsCategory,GoodsImage

for goods_detils in row_data:
    goods = Goods()
    goods.name = goods_detils['name']
    goods.goods_brief = goods_detils['desc'] if goods_detils['desc'] is not None else ""
    goods.goods_desc = goods_detils['goods_desc'] if goods_detils['goods_desc'] is not None else ""
    goods.market_price = float(int(goods_detils['market_price'].replace("￥","").replace("元","")))
    goods.shop_price = float(int(goods_detils["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_front_image = goods_detils['images'][0] if goods_detils['images'] else ""

    category_name = goods_detils['categorys'][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for image_detail in goods_detils['images']:
        image = GoodsImage()
        image.image = image_detail
        image.goods = goods
        image.save()



