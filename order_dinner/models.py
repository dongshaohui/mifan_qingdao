#coding=utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User, UserManager  
import django.utils.timezone as timezone
# Create your models here.

# 商铺
class Shop(models.Model):
	name = models.CharField(verbose_name=u'商铺名',max_length=255) # 商铺名
	search_addr = models.CharField(default='',verbose_name=u'商铺搜索地址',max_length=255) # 商铺搜索地址
	detail_addr = models.CharField(default='',verbose_name=u'商铺详细地址',max_length=255) # 商铺详细地址
	postcode = models.CharField(default='',verbose_name=u'邮编',max_length=255) # 邮编
	mobile = models.CharField(verbose_name=u'联系人电话',max_length=255) # 联系人手机
	remark = models.TextField(default='',verbose_name=u'备注信息',max_length=255) # 备注信息
	status = models.BooleanField(verbose_name=u'是否营业',default=True) # 是否营业
	shop_img = models.CharField(default='',verbose_name=u'商铺图片',max_length=255) # 商铺图片
	commission = models.FloatField(verbose_name=u'佣金百分比',default=0.0) # 佣金百分比
	def __unicode__(self):
		return self.name

# 商铺管理员
class ShopManager(User):
	shop = models.OneToOneField(Shop) # 对应店铺

# 客户
class Customer(models.Model):
	mobile = models.CharField(verbose_name=u'手机',max_length=255) # 手机
	name = models.CharField(verbose_name=u'用户名',max_length=255,default='') # 用户名
	password = models.CharField(verbose_name=u'用户密码',max_length=255) # 密码
	valid = models.BooleanField(verbose_name=u'是否可用',default=True) # 用户是否可用
	user_pay_type_id = models.IntegerField(default = 0,verbose_name=u'支付方式ID') # 默认选取支付方式ID
	delivery_address_id = models.IntegerField(default = 0,verbose_name=u'收货地址ID') # 默认收货地址ID
	create_time = models.DateTimeField(verbose_name=u'创建时间',auto_now=True)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now)

	def __unicode__(self):
		return self.name

# 支付方式
class UserPayType(models.Model):
	customer = models.ForeignKey(Customer,related_name='customer_user_pay_types') # 支付方式从属的用户
	pay_type = models.IntegerField(default = 0,verbose_name=u'支付方式') # 支付方式（0-信用卡，1-货到付款）
	credit_card = models.CharField(verbose_name=u'信用卡号',max_length=255) # 信用卡号
	security_code = models.CharField(verbose_name=u'信用安全码',max_length=255) # 信用安全码
	expire_year = models.CharField(verbose_name=u'过期年份',max_length=255) # 过期年份
	expire_month = models.CharField(verbose_name=u'过期月份',max_length=255) # 过期月份

# 收货地址
class DeliveryAddress(models.Model):
	customer = models.ForeignKey(Customer,related_name='customer_delivery_address') # 收货地址从属的用户
	receiver_name = models.CharField(verbose_name=u'收货人姓名',max_length=255,default='') # 收货人姓名
	receiver_phone = models.CharField(verbose_name=u'收货人手机',max_length=255,default='') # 收货人手机
	searched_address = models.CharField(verbose_name=u'搜索得出地址',max_length=255,default='') # 搜索得出地址
	longitude = models.FloatField(verbose_name=u'经度',default=0.0) # 经度
	latitude = models.FloatField(verbose_name=u'纬度',default=0.0) # 纬度
	detail_address = models.CharField(verbose_name=u'详细地址',max_length=255,default='') # 详细地址
	postcode = models.CharField(verbose_name=u'邮编',max_length=255,default='') # 邮编

# 信用卡
class CreditCard(models.Model):
	# customer = models.OneToOneField(Customer) # 信用卡对应客户
	cardno = models.CharField(verbose_name=u'信用卡号',max_length=255) # 信用卡号
	expire_month = models.CharField(verbose_name=u'过期月份',max_length=255) # 过期月份
	expire_year = models.CharField(verbose_name=u'过期年份',max_length=255) # 过期年份
	security_code = models.CharField(verbose_name=u'信用安全码',max_length=255) # 信用安全码


# 子菜品
class Subdish(models.Model):
	shop = models.OneToOneField(Shop) # 配菜对应商铺
	name = models.CharField(verbose_name=u'配菜名',max_length=255) # 子菜品的名称
	price = models.FloatField(verbose_name=u'配菜单价',default=0.0) # 子菜品的价格

	def __unicode__(self):
		return self.name
# 菜品
class Dish(models.Model):
	shop = models.ForeignKey(Shop,related_name='shop_dish') # 菜品隶属的商铺
	subdishes = models.ManyToManyField(Subdish,blank=True,null=True) # 菜品中包含的子菜品
 	name = models.CharField(verbose_name=u'菜名',max_length=255) # 菜品的名称
 	dish_img = models.ImageField(verbose_name=u'菜品图片',upload_to='imgs/') # 菜品的图片
	price = models.FloatField(verbose_name=u'菜品价格',default=0.0) # 菜品的价格

	def __unicode__(self):
		return self.name

# 订单
class Order(models.Model):
	customer = models.OneToOneField(Customer) # 订单对应客户
	dish = models.OneToOneField(Dish) # 订单对应的菜品
	status = models.CharField(verbose_name=u'订单状态',max_length=255) # 订单状态 -- 'PROGRESS'、'WAITPAY'、'SUCCESS'、'CLOSE'
	create_time = models.DateTimeField(verbose_name=u'创建时间',auto_now=True)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now)	
