#coding=utf-8
from django.contrib import admin
from .models import Customer,Subdish,Dish,Order,Shop,ShopManager
import xadmin
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from django.contrib.auth.models import User, UserManager  
from xadmin.plugins.batch import BatchChangeAction
# Register your models here.

class GlobalSetting(object):
    #设置base_site.html的Title
    site_title = '\"筋斗云\"后台管理'
    #设置base_site.html的Footer
    site_footer  = '\"筋斗云\"后台管理'
    def get_site_menu(self):
        return (
            {'title': '商铺管理', 'perm': self.get_model_perm(Shop, 'change'), 'menus':(
            	{'title': '商铺信息管理',  'url': self.get_model_url(Shop, 'changelist')},
            	{'title': '商铺管理员管理',  'url': self.get_model_url(ShopManager, 'changelist')},)},
            {
            	'title': '内容管理', 'perm': self.get_model_perm(Dish, 'change'), 'menus':(
                
                {'title':'配菜管理','url': self.get_model_url(Subdish, 'changelist')},
                {'title':'菜品管理','url': self.get_model_url(Dish, 'changelist')},
                {'title':'订单管理','url': self.get_model_url(Order, 'changelist')}
            )},
            {'title': '客户管理', 'perm': self.get_model_perm(Customer, 'change'), 'menus':(
            	{'title': '客户管理',  'url': self.get_model_url(Customer, 'changelist')},
            	)},            	
        )

# 定制客户管理端信息
class CustomAdmin(object):
	# fields = ('name','mobile','valid')
	list_display = ('name','mobile','valid')

# 定制配菜管理端信息
class SubdishAdmin(object):
	list_display = ('name','price','shop')

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
	list_display = ('name','price','shop','preview')

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


# 定制商铺管理员信息
class ShopManagerAdmin(object):
	def save_models(self):
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

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Customer,CustomAdmin)
xadmin.site.register(Subdish,SubdishAdmin)
xadmin.site.register(Dish,DishAdmin)
xadmin.site.register(Shop)
xadmin.site.register(Order)
xadmin.site.register(ShopManager,ShopManagerAdmin)

# xadmin.site.register(Customer,CustomAdmin)
# xadmin.site.register(views.CommAdminView, AdminMuneSetting)