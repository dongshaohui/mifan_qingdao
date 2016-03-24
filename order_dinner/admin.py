#coding=utf-8
from django.contrib import admin
from .models import Customer,Subdish,Dish,Order
import xadmin
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
# Register your models here.

class GlobalSetting(object):
    #设置base_site.html的Title
    site_title = '\"筋斗云\"后台管理'
    #设置base_site.html的Footer
    site_footer  = '\"筋斗云\"后台管理'
    def get_site_menu(self):
        return (
            {'title': '管理员内容管理', 'perm': self.get_model_perm(Customer, 'change'), 'menus':(
                {'title': '客户信息',  'url': self.get_model_url(Customer, 'changelist')},
                {'title':'配菜信息','url': self.get_model_url(Subdish, 'changelist')},
                {'title':'菜品信息','url': self.get_model_url(Dish, 'changelist')},
                {'title':'订单信息','url': self.get_model_url(Order, 'changelist')}
            )},
        )

# 定制客户管理端信息
class CustomAdmin(object):
	# fields = ('name','mobile','valid')
	list_display = ('name','mobile','valid')

# 定制配菜管理端信息
class SubdishAdmin(object):
	list_display = ('name','price')

# 定制配菜管理端信息
class DishAdmin(object):
	list_display = ('id','name','price')

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Customer,CustomAdmin)
xadmin.site.register(Subdish,SubdishAdmin)
xadmin.site.register(Dish,DishAdmin)
xadmin.site.register(Order)
# xadmin.site.register(Customer,CustomAdmin)
# xadmin.site.register(views.CommAdminView, AdminMuneSetting)