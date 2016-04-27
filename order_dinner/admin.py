#coding=utf-8
from django.contrib import admin
from .models import Customer,Subdish,Dish,Order,Shop,ShopManager,BannerImg,GlobalSetting,UserPayType
import xadmin
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from django.contrib.auth.models import User, UserManager  
from xadmin.plugins.batch import BatchChangeAction
# Register your models here.

class GlobalViewSetting(object):
    #设置base_site.html的Title
    site_title = '\"筋斗云\"后台管理'
    #设置base_site.html的Footer
    site_footer  = '\"筋斗云\"后台管理'
    def get_site_menu(self):
        return (
            {'title': '商铺管理', 'perm': self.get_model_perm(Shop, 'change'), 'menus':(
            	{'title': '全局参数管理',  'url': self.get_model_url(GlobalSetting, 'changelist')},
            	{'title': '商铺信息管理',  'url': self.get_model_url(Shop, 'changelist')},
            	{'title': '商铺管理员管理',  'url': self.get_model_url(ShopManager, 'changelist')},
            	# {'title': '超级管理员菜品管理',  'url': self.get_model_url(Dish, 'changelist')},
              )
            },
            {
            	'title': '内容管理', 'perm': self.get_model_perm(Dish, 'change'), 'menus':(
                
                {'title':'配菜管理','url': self.get_model_url(Subdish, 'changelist')},
                {'title':'菜品管理','url': self.get_model_url(Dish, 'changelist')},
                {'title':'订单管理','url': self.get_model_url(Order, 'changelist')},
                
            )},
            {'title': '客户管理', 'perm': self.get_model_perm(Customer, 'change'), 'menus':(
            	{'title': '客户管理',  'url': self.get_model_url(Customer, 'changelist')},
            	{'title':'Banner图管理','url': self.get_model_url(BannerImg, 'changelist')},
            	{'title':'支付方式管理','url': self.get_model_url(UserPayType, 'changelist')},
            	
            	)},            	
        )

# 定制客户管理端信息
class CustomAdmin(object):
	# fields = ('name','mobile','valid')
	list_display = ('name','mobile','valid')
	list_filter = ('create_time',)
# 定制配菜管理端信息
class SubdishAdmin(object):
	list_display = ('name','price','shop')

	def get_model_form(self, **kwargs):
		form = super(SubdishAdmin, self).get_model_form(**kwargs)
		# print self.user.id
		shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
		shop = Shop.objects.get(id=shop_id)
		form.base_fields['shop'].queryset = Shop.objects.filter(id=shop_id)
		return form
	# 为显示增加外键项
	# def get_shop_name(self,obj):
	# 	return obj.shop.name
	# shop.short_description = "所属店家"
	# 客户查询过滤
	def get_list_queryset(self):
		print "current user id = ", self.user.id
		# 判断是否为超级用户
		if not self.user.is_superuser:
			# 获取shop id
			current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
			return super(SubdishAdmin,self).get_list_queryset().filter(shop_id=current_shop_id)
		else:
			return super(SubdishAdmin,self).get_list_queryset()
			

# 定制菜品管理端信息
class DishAdmin(object):
	fields = ('name','price','dish_type','subdishes','name','name_en','dish_img')
	list_display = ('name','price','shop','preview')

	# def changelist_view(self):
	# 	print "changelist"

	def get_model_form(self, **kwargs):
		form = super(DishAdmin, self).get_model_form(**kwargs)
		# print self.user.id
		shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
		form.base_fields['subdishes'].queryset = Subdish.objects.filter(shop_id=shop_id)
		return form


	def preview(self,obj):
		return '<img src="/media/%s" height="80" width="100" />' %(obj.dish_img)
	preview.allow_tags = True
	preview.short_description = "菜品图片"
	# 客户查询过滤
	def get_list_queryset(self):
		print "current user id = ", self.user.id
		# 判断是否为超级用户
		if not self.user.is_superuser:
			# 获取shop id
			current_shop_id = ShopManager.objects.get(user_ptr_id=self.user.id).shop_id
			return super(DishAdmin,self).get_list_queryset().filter(shop_id=current_shop_id)
		else:
			return super(DishAdmin,self).get_list_queryset()

	# 保存model
	def save_models(self):
		obj = self.new_obj
		request = self.request
		dish_id = obj.id
		author_id = request.user.id
		shop_id = ShopManager.objects.get(user_ptr_id=author_id).shop_id
		obj.shop_id = shop_id
		obj.save()
		# print "author_id",author_id

class OrderAdmin(object):
	def order_state_view(self,obj):
		print "self status = ", self.status
		if self.status == "PROGRESS":
			return u"进行中"
		elif self.status == "ACCEPTED":
			return u"已接受"
		elif self.status == "SUCCESS":
			return u"已完成"
		elif self.status == "CLOSE":
			return u"已取消"
	order_state_view.allow_tags = True
	order_state_view.short_description = "订单状态"	
	# fields = ('name','mobile','valid')
	list_display = ('customer','shop','order_dishes','delivery_address','status','tip','freight','tax','total_price')
	list_filter = ('create_time','status')
# 定制商铺管理员信息
class ShopManagerAdmin(object):
	def save_models(self):
		print self.new_obj.user_ptr_id
		self.new_obj.save()
		current_user_id = self.new_obj.user_ptr_id
		current_shop_id = self.new_obj.shop_id
		current_obj = self.new_obj
		current_user = User.objects.get(id=current_user_id)
		current_user.set_password(self.new_obj.password)
		# print current_user.password
		current_obj.password = current_user.password
		current_obj.save()
		# new_user = self.new_obj.user_ptr
		# print new_user.name
		# print self.new_obj.password
		# print self.new_obj
		# print self.new_obj.user_ptr_id
		# print current_shop_id

# 定制Banner图管理
class BannerImgAdmin(object):
	def preview(self,obj):
		return '<img src="/media/%s" height="80" width="100" />' %(obj.img)	
	preview.allow_tags = True
	preview.short_description = "banner展示图（缩略图）"		
	# fields = ('name','mobile','valid')
	list_display = ('name','preview','priority','link')

# 定制全局参数管理
class GlobalSettingAdmin(object):
	fields = ("freight_thres","tax_rate","discount_rate")
	list_display = ("freight_thres","tax_rate","discount_rate")

# 商铺管理
class ShopAdmin(object):
	fields = ("name","name_en","postcode",'mobile','business_hour','remark','remark_en','shop_img','shop_feature','shop_feature_en','commission')
	list_display = ("name","name_en","postcode",'mobile','business_hour','remark','remark_en','shop_img','shop_feature','shop_feature_en','commission','registration_id')


class UserPayTypeAdmin(object):
	fields = ("customer","pay_type","credit_card","security_code","expire_year","expire_month")
	list_display = ("id","customer","pay_type","credit_card","security_code","expire_year","expire_month")

xadmin.site.register(views.CommAdminView, GlobalViewSetting)
xadmin.site.register(Customer,CustomAdmin)
xadmin.site.register(Subdish,SubdishAdmin)
xadmin.site.register(Dish,DishAdmin)
xadmin.site.register(Shop,ShopAdmin)
xadmin.site.register(Order,OrderAdmin)
xadmin.site.register(ShopManager,ShopManagerAdmin)
xadmin.site.register(BannerImg,BannerImgAdmin)
xadmin.site.register(GlobalSetting,GlobalSettingAdmin)
xadmin.site.register(UserPayType,UserPayTypeAdmin)
# xadmin.site.register(Customer,CustomAdmin)
# xadmin.site.register(views.CommAdminView, AdminMuneSetting)