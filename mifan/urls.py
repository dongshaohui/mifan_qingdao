#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mifan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jdy_admin/', include(xadmin.site.urls)),
    # url(r'^admin/', include(admin.site.urls)),

    # 商家端接口（Android）
    url(r'^shop_serv/login','shop_serv.views.login'),
    url(r'^shop_serv/modify_business_status','shop_serv.views.modify_business_status'),
    url(r'^shop_serv/entry_addr_status','shop_serv.views.entry_addr_status'),
    url(r'^shop_serv/reject_new_order','shop_serv.views.reject_new_order'),
    url(r'^shop_serv/accept_new_order','shop_serv.views.accept_new_order'),
    url(r'^shop_serv/finish_order','shop_serv.views.finish_order'),
    url(r'^shop_serv/personal_info','shop_serv.views.personal_info'),
    url(r'^shop_serv/get_all_finish_orders','shop_serv.views.get_all_finish_orders'),
    url(r'^shop_serv/get_all_accept_orders','shop_serv.views.get_all_accept_orders'),
    url(r'^shop_serv/get_all_new_orders','shop_serv.views.get_all_new_orders'),
    url(r'^shop_serv/get_all_history_orders','shop_serv.views.get_all_history_orders'),
    url(r'^shop_serv/search_orders','shop_serv.views.search_orders'),
    url(r'^shop_serv/upload_addr','shop_serv.views.upload_addr'),
    url(r'^shop_serv/get_addr','shop_serv.views.get_addr'), 
         
    # 客户端接口（IOS）
    ########################### 
    #
    #   User Module
    #
    ###########################     
    url(r'^user_serv/register','user_serv.views.register'), 
    url(r'^user_serv/login','user_serv.views.login'), 
    url(r'^user_serv/send_verification_code','user_serv.views.send_verification_code'), 
    url(r'^user_serv/drop_user','user_serv.views.drop_user'), 
    # url(r'^user_serv/get_verification_code','user_serv.views.get_verification_code'), 
    ########################### 
	#
	#	User_Pay_Type_Module
	#
	########################### 
    url(r'^user_serv/personal_info','user_serv.views.personal_info'), 
    url(r'^user_serv/add_credit_card','user_serv.views.add_credit_card'), 
    url(r'^user_serv/select_paytype','user_serv.views.select_paytype'), 
    url(r'^user_serv/paytype_infos','user_serv.views.paytype_infos'), 
    url(r'^user_serv/get_paytype','user_serv.views.get_paytype'), 
    url(r'^user_serv/delete_paytype','user_serv.views.delete_paytype'), 
	########################### 
	#
	#	USER ADDRESS MODULE
	#
	########################### 
    url(r'^user_serv/site_search','user_serv.views.site_search'), 
	url(r'^user_serv/add_delivery_address','user_serv.views.add_delivery_address'), 
	url(r'^user_serv/select_delivery_address','user_serv.views.select_delivery_address'), 
	url(r'^user_serv/delivery_address_infos','user_serv.views.delivery_address_infos'), 
	url(r'^user_serv/get_user_delivery_address','user_serv.views.get_user_delivery_address'), 
    url(r'^user_serv/delete_delivery_address','user_serv.views.delete_delivery_address'), 
    url(r'^user_serv/edit_delivery_address','user_serv.views.delete_delivery_address'), 
	########################### 
	#
	#	SHOP MODULE
	#
	########################### 
	url(r'^user_serv/search_shop_infos','user_serv.views.search_shop_infos'), 
    url(r'^user_serv/get_shop_detail_info','user_serv.views.get_shop_detail_info'), 
    url(r'^user_serv/get_all_shop_infos','user_serv.views.get_all_shop_infos'), 
    ########################### 
    #
    #   Dish Module Interface
    #
    ###########################     
    url(r'^user_serv/get_all_side_dishes','user_serv.views.get_all_side_dishes'), 
    url(r'^user_serv/search_dishes','user_serv.views.search_dishes'),\
    url(r'^user_serv/get_dish_detail','user_serv.views.get_dish_detail'),
    ########################### 
    #
    #   Order Module Interface
    #
    ###########################     
    url(r'^user_serv/upload_order','user_serv.views.upload_order'),
    url(r'^user_serv/get_all_orders','user_serv.views.get_all_orders'),
    url(r'^user_serv/get_order_detail_info','user_serv.views.get_order_detail_info'),
    url(r'^user_serv/calculate_distance','user_serv.views.calculate_distance'),

    # 提交订单
    url(r'^user_serv/calculate_freight','user_serv.views.calculate_freight'), # 计算运费
    url(r'^user_serv/calculate_tax','user_serv.views.calculate_tax'), # 计算税
    # url(r'^user_serv/calculate_tip','user_serv.views.calculate_tip'), # 计算小费

    ########################### 
    #
    #   OTHER MODULE
    #
    ########################### 
    url(r'^user_serv/get_banner_list','user_serv.views.get_banner_list'),
    url(r'^user_serv/delete_token','user_serv.views.delete_token'),
    url(r'^user_serv/get_global_conf','user_serv.views.get_global_conf'),
)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   
