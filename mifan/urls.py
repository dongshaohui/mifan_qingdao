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
    url(r'^xadmin/', include(xadmin.site.urls)),
    # url(r'^admin/', include(admin.site.urls)),

    # 商家端接口（Android）
    url(r'^shop_serv/login','shop_serv.views.login'),
    # 客户端接口（IOS）
    url(r'^user_serv/register','user_serv.views.register'), 
    url(r'^user_serv/login','user_serv.views.login'), 
    url(r'^user_serv/personal_info','user_serv.views.personal_info'), 
)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   
