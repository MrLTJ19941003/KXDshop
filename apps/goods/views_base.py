# encoding: utf-8
"""
@version: 1.0
@author: liutj
@software: PyCharm
@file: adminx.py
@time: 2018/7/17 17:04
"""

from django.views.generic.base import View
from goods.models import Goods


class GoodsListView(View):
    def get(self,request):
        '''
        通过django的view实现商品列表页
        :param request:
        :return:
        '''
        #json_list = []

        # for good in goods:
        #     json_dict = {}
        #     json_dict["name"] = good.name
        #     json_dict["category"] = good.category.name
        #     json_dict["market_price"] = good.market_price
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        import json
        goods = Goods.objects.all()[:10]

        from django.core import serializers
        json_data = serializers.serialize("json",goods)
        json_data = json.loads(json_data)

        from django.http import HttpResponse,JsonResponse
        return JsonResponse(json_data,safe=False)
        #return HttpResponse(json.dumps(json_data),content_type="application/json")