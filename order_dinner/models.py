#coding=utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User, UserManager  
import django.utils.timezone as timezone
# Create your models here.



# 超级管理员全局设置
class GlobalSetting(models.Model):
	freight_thres = models.FloatField(verbose_name=u'满X元免运费',default=0.0)
	tax_rate = models.FloatField(verbose_name=u'税率',default=0.08)
	discount_rate = models.FloatField(verbose_name=u'折扣率',default=0.0)
	customer_service = models.CharField(verbose_name=u'客服电话',max_length=255,default="")
	policy_link = models.CharField(verbose_name=u'协议链接地址',max_length=255,default="")
	working_hours = models.CharField(verbose_name=u'工作时间设置',max_length=255,default="")

	class Meta:
		verbose_name = '全局设置'
		verbose_name_plural  = '全局设置'
		# ordering = ['-priority']	



# 商铺营业状态
class ShopBusinessStatus(models.Model):
	desc = models.CharField(verbose_name=u'状态描述',max_length=255) 
	status_tag =  models.IntegerField(verbose_name=u'是否营业',default=1) # 是否营业（0-未营业 1-营业）

	class Meta:
		verbose_name = '商铺营业状态'
		verbose_name_plural  = '商铺营业状态'
		# ordering = ['-priority']	

	def __unicode__(self):
		return self.desc

# 商铺
class Shop(models.Model):
	name = models.CharField(verbose_name=u'商铺中文名',max_length=255) # 商铺名
	name_en = models.CharField(default='',verbose_name=u'商铺英文名',max_length=255) # 商铺名
	search_addr = models.CharField(default='',verbose_name=u'商铺搜索地址',max_length=255) # 商铺搜索地址
	detail_addr = models.CharField(default='',verbose_name=u'商铺详细地址',max_length=255) # 商铺详细地址
	longitude = models.FloatField(verbose_name=u'经度',default=0.0) # 经度
	latitude = models.FloatField(verbose_name=u'纬度',default=0.0) # 纬度	
	postcode = models.CharField(default='',verbose_name=u'邮编',max_length=255) # 邮编
	mobile = models.CharField(verbose_name=u'联系人电话',max_length=255) # 联系人手机
	business_hour = models.CharField(verbose_name=u'营业时间',max_length=255) # 营业时间
	remark = models.TextField(default='',verbose_name=u'备注中文信息',max_length=255) # 备注信息
	remark_en = models.TextField(default='',verbose_name=u'备注英文信息',max_length=255) # 备注信息英文
	status = models.IntegerField(verbose_name=u'是否营业',default=1) # 是否营业（0-未营业 1-营业）
	shop_img = models.ImageField(verbose_name=u'商铺图片',upload_to='imgs/') # 商铺图片
	shop_feature = models.CharField(default='',verbose_name=u'商店特色中文',max_length=255) # 商店特色
	shop_feature_en = models.CharField(default='',verbose_name=u'商店特色英文',max_length=255) # 商店英文特色
	commission = models.FloatField(verbose_name=u'佣金百分比',default=0.1) # 佣金百分比
	min_distribution_cost = models.FloatField(verbose_name=u'最低配送费用',default=0.0) # 最低配送费用
	registration_id = models.CharField(default='',verbose_name=u'极光推送ID',max_length=255) # 极光推送ID
	# discount = models.FloatField(verbose_name=u'折扣',default=0.0) # 折扣
	class Meta:
		verbose_name = '商店'
		verbose_name_plural  = '商店'
		# ordering = ['-priority']	

	def __unicode__(self):
		return self.name

# 佣金设置
# class CommissionSetting(models.Model):
	
# 	class Meta:
# 		verbose_name = '商店'
# 		verbose_name_plural  = '商店'
# 		# ordering = ['-priority']	

# 	def __unicode__(self):
# 		return self.name


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

	class Meta:
		verbose_name = '用户'
		verbose_name_plural  = '用户'
		ordering = ['-create_time']	

	def __unicode__(self):
		return self.mobile

# 手机验证码记录
class VerificationCode(models.Model):
	mobile = models.CharField(verbose_name=u'手机',max_length=255) # 手机
	verification_code = models.CharField(verbose_name=u'手机验证码',max_length=255,default='') # 手机验证码



# 支付方式
class UserPayType(models.Model):
	customer = models.ForeignKey(Customer,related_name='customer_userpaytype',blank=True,null=True) # 支付方式从属的用户
	pay_type = models.IntegerField(default = 0,verbose_name=u'支付方式（0-信用卡，1-货到付款）') # 支付方式（0-信用卡，1-货到付款）
	credit_card = models.CharField(verbose_name=u'信用卡号',max_length=255) # 信用卡号
	security_code = models.CharField(verbose_name=u'信用安全码',max_length=255) # 信用安全码
	expire_year = models.CharField(verbose_name=u'过期年份',max_length=255) # 过期年份
	expire_month = models.CharField(verbose_name=u'过期月份',max_length=255) # 过期月份
	class Meta:
		verbose_name = '用户支付方式'
		verbose_name_plural  = '用户支付方式'
		# ordering = ['-create_time']	

	def __unicode__(self):
		if self.customer:
			return self.customer.mobile + " " + str(self.pay_type) + " " + self.credit_card
		else:
			return str(self.pay_type) + " " + self.credit_card
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

	class Meta:
		verbose_name = '收货地址'
		verbose_name_plural  = '收货地址'
		# ordering = ['-create_time']	

	def __unicode__(self):
		return self.receiver_name

# 信用卡
class CreditCard(models.Model):
	# customer = models.OneToOneField(Customer) # 信用卡对应客户
	cardno = models.CharField(verbose_name=u'信用卡号',max_length=255) # 信用卡号
	expire_month = models.CharField(verbose_name=u'过期月份',max_length=255) # 过期月份
	expire_year = models.CharField(verbose_name=u'过期年份',max_length=255) # 过期年份
	security_code = models.CharField(verbose_name=u'信用安全码',max_length=255) # 信用安全码



# banner图片
class BannerImg(models.Model):
	name = models.CharField(default="",verbose_name=u'轮播图片名',max_length=255) # 图片名称
	link = models.CharField(default="",blank=True,null=True,verbose_name=u'超链接',max_length=255) # 超链接
	img = models.ImageField(verbose_name=u'轮播图片',upload_to='imgs/') # 轮播图片
	priority = models.IntegerField(verbose_name=u'优先级(优先级高的优先显示)',default=0) # 优先级

	class Meta:
		verbose_name = '轮播图'
		verbose_name_plural  = '轮播图'
		ordering = ['-priority']	

	def __unicode__(self):
		return self.name

# 子菜品
class Subdish(models.Model):
	shop = models.ForeignKey(Shop) # 配菜对应商铺
	name = models.CharField(default='',verbose_name=u'配菜中文名',max_length=255) # 子菜品的中文名称
	name_en = models.CharField(default='',verbose_name=u'配菜英文名',max_length=255) # 子菜品的英文名称
	price = models.FloatField(verbose_name=u'配菜单价',default=0.0) # 子菜品的价格

	class Meta:
		verbose_name = '配菜'
		verbose_name_plural  = '配菜'

	def __unicode__(self):
		return self.name
# 菜品
class Dish(models.Model):
	shop = models.ForeignKey(Shop,related_name='shop_dish',verbose_name="选取店铺") # 菜品隶属的商铺
	dish_type = models.IntegerField(verbose_name=u'菜品类型（0-单品菜，1-含配菜）',default=0) # （0-单品菜，1-含配菜）
	subdishes = models.ManyToManyField(Subdish,blank=True,null=True,verbose_name="选取子菜品") # 菜品中包含的子菜品
 	name = models.CharField(default='',verbose_name=u'中文菜名',max_length=255) # 中文菜品的名称
 	name_en = models.CharField(default='',verbose_name=u'英文菜名',max_length=255) # 英文菜品的名称
 	dish_img = models.ImageField(verbose_name=u'菜品图片',upload_to='imgs/') # 菜品的图片
	price = models.FloatField(verbose_name=u'菜品价格',default=0.0) # 菜品的价格
	dish_order_checkout_thres = models.FloatField(verbose_name=u'菜品成菜价格下限（只对含配菜有效）',default=0.0) #菜品成菜价格下限（只对含配菜有效）
	class Meta:
		verbose_name = '菜品'
		verbose_name_plural  = '菜品'
		# ordering = ['-priority']	

	def __unicode__(self):
		return self.name

# 订单中的子菜品
class OrderSubDish(models.Model):
	subdish = models.ForeignKey(Subdish) # 对应的子菜品
	subdish_order_number = models.IntegerField(verbose_name=u'子菜品点单次数',default=0) 

# 订单中的菜品
class OrderDish(models.Model):
	dish = models.ForeignKey(Dish,related_name='order_dish')  # 订单中菜品对应的菜品
	dish_order_number = models.IntegerField(verbose_name=u'菜品点单次数',default=0) 
	ordered_subdishes = models.ManyToManyField(OrderSubDish,blank=True,null=True) # 订单中菜品包含的子菜品


	class Meta:
		verbose_name = '订单中的菜品'
		verbose_name_plural  = '订单中的菜品'
		# ordering = ['-create_time']	

	def __unicode__(self):
		return self.dish.name 


# 订单
class Order(models.Model):
	customer = models.ForeignKey(Customer,related_name="customer_order",verbose_name="用户手机") # 订单对应客户
	shop = models.ForeignKey(Shop,related_name="shop_order",verbose_name="店铺") # 订单对应商铺
	order_dishes = models.ManyToManyField(OrderDish,blank=True,null=True,verbose_name="订单包含菜品") # 订单包含的菜品
	delivery_address = models.ForeignKey(DeliveryAddress,related_name="delivery_address_order",blank=True,null=True,verbose_name="送货地址") # 订单对应的地址
	pay_type = models.ForeignKey(UserPayType,verbose_name=u'支付方式',blank=True,null=True) # 订单对应的支付方式
	consume_type =  models.IntegerField(verbose_name=u'消费方式（0-配送，1-到店消费）',default=0) # （0-配送，1-到店消费）
	freight = models.FloatField(verbose_name=u'订单运费',default=0.0) # 订单运费
	commission_price = models.FloatField(verbose_name=u'佣金',default=0.0) # 佣金
	discount_price = models.FloatField(verbose_name=u'折扣金额',default=0.0) # 折扣金额
	tip_type = models.IntegerField(verbose_name=u'小费方式（0-小费比率，1-现金小费）',default=0) # （0-小费比率，1-现金小费）
	tax = models.FloatField(verbose_name=u'订单税费',default=0.0) # 订单税费
	distance = models.FloatField(verbose_name=u'订单距离',default=0.0) # 订单距离
	remark = models.CharField(verbose_name=u'订单备注',max_length=255) # 订单备注
	tip = models.FloatField(verbose_name=u'订单小费',default=0.0) # 订单小费
	status = models.CharField(verbose_name=u'订单状态',max_length=255) # 订单状态 -- 'PROGRESS'、'ACCEPTED'、'SUCCESS'、'CLOSE'
	reject_reason = models.CharField(verbose_name=u'订单取消原因',max_length=255,default='') # 订单取消原因
	total_price = models.FloatField(verbose_name=u'订单总价格',default=0.0) # 订单总价格
	origin_price = models.FloatField(verbose_name=u'菜品总价格',default=0) # 菜品总价格
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)

	class Meta:
		verbose_name = '订单'
		verbose_name_plural  = '订单'
		ordering = ['-create_time']	

	# def __unicode__(self):
	# 	return self.name