#coding=utf-8
from django.db import models
from datetime import datetime
import django.utils.timezone as timezone
# Create your models here.

# 客户
class Customer(models.Model):
	mobile = models.CharField(max_length=255) # 手机
	name = models.CharField(max_length=255) # 用户名
	password = models.CharField(max_length=255) # 密码
	valid = models.BooleanField(default=True) # 用户是否可用
	# create_time = models.DateTimeField(auto_now=True)
	# update_time = models.DateTimeField(default=timezone.now)

# 子菜品
class Subdish(models.Model):
	name = models.CharField(max_length=255) # 子菜品的名称
	price = models.FloatField(default=0.0) # 子菜品的价格

# 菜品
class Dish(models.Model):
	subdishes = models.ManyToManyField(Subdish) # 菜品中包含的子菜品
 	name = models.CharField(max_length=255) # 菜品的名称
 	dish_img = models.ImageField(upload_to='imgs/') # 菜品的图片
	price = models.FloatField(default=0.0) # 菜品的价格 	

# 订单
class Order(models.Model):
	customer = models.OneToOneField(Customer) # 订单对应客户
	dish = models.OneToOneField(Dish) # 订单对应的菜品
	status = models.CharField(max_length=255) # 订单状态 -- 'PROGRESS'、'WAITPAY'、'SUCCESS'、'CLOSE'
	# create_time = models.DateTimeField(auto_now=True)
	# update_time = models.DateTimeField(default=timezone.now)	
