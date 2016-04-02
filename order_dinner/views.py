#coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect
import urllib,urllib2,json,time,random

# 商户登录
def login(request):
	response = {}
	return HttpResponse(json.dumps(response))

# 获取所有新订单
def get_all_new_orders(request):
	response = {}
	return HttpResponse(json.dumps(response))