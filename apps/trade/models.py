from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from goods.models import Goods

user = get_user_model()


class ShopingCart(models.Model):
    '''
    购物车
    '''
    user = models.ForeignKey(user,verbose_name=u"用户")
    goods = models.ForeignKey(Goods,verbose_name=u"商品")
    nums = models.IntegerField(default=0,verbose_name="购买数量")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return '%S(%d)'.format(self.goods.name,self.nums)


class OrderInfo(models.Model):
    '''
    订单
    '''
    ORDER_STATUS = (
        ('TRADE_SUCCESS','支付成功'),
        ('TRADE_CLOSED','超时关闭'),
        ('TRADE_FINISHED','交易完结'),
        ('WAIT_BUYER_PAY', '交易创建'),
    )
    user = models.ForeignKey(user,verbose_name="用户")
    order_sn = models.CharField(max_length=30,unique=True,null=True,blank=True,verbose_name="订单号")
    trade_no = models.CharField(max_length=100,unique=True,null=True,blank=True, verbose_name="交易订单号")
    pay_status = models.CharField(choices=ORDER_STATUS,max_length=30,default="WAIT_BUYER_PAY", verbose_name="订单状态")
    post_script = models.CharField(max_length=200, verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True,blank=True,verbose_name="支付时间")

    # 用户信息
    address = models.CharField(max_length=100,default="",verbose_name="收货地址")
    signer_name = models.CharField(max_length=20,default="",verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11,verbose_name="联系电话")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    '''
    订单的商品详情
    '''
    order = models.ForeignKey(OrderInfo,verbose_name="订单信息",related_name="goods")
    goods = models.ForeignKey(Goods,verbose_name="商品")
    goods_num = models.IntegerField(default=0,verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单的商品详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)