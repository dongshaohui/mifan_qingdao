#coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
import urllib,urllib2,json,time
from order_dinner.models import Customer,UserPayType,DeliveryAddress,ShopManager,Shop,Dish,Subdish,VerificationCode,Order,OrderDish,OrderSubDish
from random import Random
from django.contrib import auth
from django.views.decorators.http import require_POST
import datetime
# Create your views here.

# @require_POST
def login(request):
	response = {}
	username = None
	password = None
	code = None
	registration_id = None
	# 获取用户名
	if 'username' in request.GET:
		username = request.GET['username']
	else:
		code = -100

	# 获取密码
	if 'password' in request.GET:
		password = request.GET['password']
	else:
		code = -100

	# 极光推送ID
	if 'registration_id' in request.GET:
		registration_id = request.GET['registration_id']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	user = auth.authenticate(username=username, password=password)
	if user is not None:
		user_id = (int)(user.id)
		shop_manager = ShopManager.objects.get(user_ptr_id=user_id)
		shop_id = shop_manager.shop_id
		shop_obj = Shop.objects.get(id=shop_id)
		shop_obj.registration_id = registration_id
		shop_obj.save()
		# print shop_id,"shop_id"
		token = token_str() # 生成token
		request.session[token] = shop_id # 存入session中
		response = {'code':0,'msg':'Success','token':token} 		
	else:
		response = {"code": -1, "msg":"用户名或密码不正确，请重试"}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 修改营业状态
def modify_business_status(request):
	response = {}
	token = None
	business_status = None

	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if 'business_status' in request.GET:
		business_status = request.GET['business_status']
	else:
		code = -100	

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)
	shop_obj.status = int(business_status)
	shop_obj.save()
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 判断商户是否录入过地址
def entry_addr_status(request):
	response = {}
	token = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)
	if shop_obj.search_addr == '' or len(shop_obj.search_addr) == 0:
		response = {'code':0,'msg':'没有录入过'}
	else:	
		response = {'code':1,'msg':'录入过地址'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 拒绝新订单
def reject_new_order(request):
	response = {}
	token = None
	orderid = None
	reason = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100

	if 'orderid' in request.GET:
		orderid = request.GET['orderid']
	else:
		code = -100		

	if 'reason' in request.GET:
		reason = request.GET['reason']
	else:
		code = -100		


	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)	

	# 查看orderid是否存在
	orders = Order.objects.filter(id=orderid)
	if len(orders) == 0:
		response = {'code':-2,'msg':'订单id不存在'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	order_obj = orders[0]
	if str(order_obj.status) != "PROGRESS":
		response = {'code':-3,'msg':'订单id不是新订单id'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 更新订单状态
	order_obj.status = "CLOSE"
	order_obj.reject_reason = reason
	order_obj.save()
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 接新订单
def accept_new_order(request):
	response = {}
	token = None
	orderid = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100

	if 'orderid' in request.GET:
		orderid = request.GET['orderid']
	else:
		code = -100			

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)	

	# 查看orderid是否存在
	orders = Order.objects.filter(id=orderid)
	if len(orders) == 0:
		response = {'code':-2,'msg':'订单id不存在'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	order_obj = orders[0]
	if str(order_obj.status) != "PROGRESS":
		response = {'code':-3,'msg':'订单id不是新订单id'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 更新订单状态
	order_obj.status = "ACCEPTED"
	order_obj.save()	
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 完成订单
def finish_order(request):
	response = {}
	token = None
	orderid = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100

	if 'orderid' in request.GET:
		orderid = request.GET['orderid']
	else:
		code = -100			


	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)	

	# 查看orderid是否存在
	orders = Order.objects.filter(id=orderid)
	if len(orders) == 0:
		response = {'code':-2,'msg':'订单id不存在'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	order_obj = orders[0]
	if str(order_obj.status) != "ACCEPTED":
		response = {'code':-3,'msg':'订单id不是已完成订单id'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 更新订单状态
	order_obj.status = "SUCCESS"
	order_obj.save()	
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 获取商户的信息
def personal_info(request):
	response = {}
	token = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)	
	response = {'code':0,'msg':'success'}
	response['business_status'] = shop_obj.status
	response['username'] = shop_obj.name
	response['phoneno'] = shop_obj.mobile
	response['shopimg']  = "http://resource.jindouyunonline.com:8001/media/" + shop_obj.shop_img.name
	response['addr'] = shop_obj.search_addr + ' ' + shop_obj.detail_addr
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取所有已完成订单
def get_all_finish_orders(request):
	response = {}
	token = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)
	print shop_obj.name,shop_obj.id
	# 获取已经完成的订单
	orders = Order.objects.filter(shop_id=shop_id,status="SUCCESS")
	totol_order_number = len(orders)
	pageno = 1
	pagelength = len(orders)

	if "pageno" in request.GET:
		if int(request.GET['pageno']) > 0:
			pageno = int(request.GET['pageno'])
	if "pagelength" in request.GET:
		pagelength = int(request.GET['pagelength'])

	orders = orders[(pageno-1)*pagelength:pageno*pagelength]

	response = {'code':0,'msg':'success'}
	response['orders'] = {}
	response['orders']['count'] = totol_order_number
	order_list = []
	for order in orders:
		temp_order_obj = {}
		temp_order_obj['orderid'] = order.id
		temp_order_obj['order_status'] = 3
		temp_order_obj['ordertime'] = datetime.datetime.strftime(order.create_time,'%Y-%m-%d %H:%M:%S')
		userinfo = {}

		customer = Customer.objects.get(id=order.customer_id) # 获取订单对应用户
		userinfo['name'] = customer.name
		userinfo['phoneno'] = customer.mobile
		temp_order_obj['userinfo'] = userinfo

		# 地址
		delivery_address = DeliveryAddress.objects.get(id=order.delivery_address_id) # 获取订单对应地址信息
		temp_order_obj['orderaddr'] = delivery_address.searched_address + ' ' + delivery_address.detail_address 
		temp_order_obj['sendtype'] = order.consume_type

		# 支付信息
		pay_type_obj = UserPayType.objects.get(id=order.pay_type_id)
		temp_order_obj['paytype'] = pay_type_obj.pay_type
		creditcard_info = {}
		if int(pay_type_obj.pay_type) == 0:
			creditcard_info['cardno'] = pay_type_obj.credit_card
			creditcard_info['pin'] = pay_type_obj.security_code
			creditcard_info['validate_year'] = pay_type_obj.expire_year
			creditcard_info['validate_month'] = pay_type_obj.expire_month
		temp_order_obj['creditcard_info'] = creditcard_info

		# 菜品详情
		dishinfos = []
		for order_dish in order.order_dishes.all():
			temp_dish_obj = {}
			temp_dish_obj['dish_number'] = order_dish.dish_order_number
			temp_dish_obj['dish_name'] = order_dish.dish.name
			temp_dish_obj['dish_type'] = order_dish.dish.dish_type
			temp_dish_obj['dish_price'] = order_dish.dish.price
			sub_dish_list = []
			if int(order_dish.dish.dish_type) == 1:
				for subdish in order_dish.dish.subdishes.all():
					temp_subdish_obj = {}
					temp_subdish_obj['name'] = subdish.name
					temp_subdish_obj['price'] = subdish.price
					sub_dish_list.append(temp_subdish_obj)
			temp_dish_obj['sub_dish_list'] = sub_dish_list
			dishinfos.append(temp_dish_obj)
		temp_order_obj['dishinfos'] = dishinfos

		# 订单价格详情
		price_detail = {}
		price_detail['dish_total_price'] = order.total_price
		price_detail['tax_price'] = order.tax
		price_detail['freight_price'] = order.freight
		price_detail['tip_price'] = order.tip
		temp_order_obj['price_detail'] = price_detail
		order_list.append(temp_order_obj)
	response['orders']['list'] = order_list
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 获取所有已历史订单
def get_all_history_orders(request):
	response = {}
	token = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)
	print shop_obj.name,shop_obj.id
	# 获取已经完成的订单
	orders = Order.objects.filter(shop_id=shop_id,status="SUCCESS").filter(create_time__lt=datetime.date.today())
	totol_order_number = len(orders)
	pageno = 1
	pagelength = len(orders)

	if "pageno" in request.GET:
		if int(request.GET['pageno']) > 0:
			pageno = int(request.GET['pageno'])
	if "pagelength" in request.GET:
		pagelength = int(request.GET['pagelength'])

	orders = orders[(pageno-1)*pagelength:pageno*pagelength]

	response = {'code':0,'msg':'success'}
	response['orders'] = {}
	response['orders']['count'] = totol_order_number
	order_list = []
	for order in orders:
		temp_order_obj = {}
		temp_order_obj['orderid'] = order.id
		temp_order_obj['order_status'] = 3
		temp_order_obj['ordertime'] = datetime.datetime.strftime(order.create_time,'%Y-%m-%d %H:%M:%S')
		userinfo = {}

		customer = Customer.objects.get(id=order.customer_id) # 获取订单对应用户
		userinfo['name'] = customer.name
		userinfo['phoneno'] = customer.mobile
		temp_order_obj['userinfo'] = userinfo

		# 地址
		delivery_address = DeliveryAddress.objects.get(id=order.delivery_address_id) # 获取订单对应地址信息
		temp_order_obj['orderaddr'] = delivery_address.searched_address + ' ' + delivery_address.detail_address 
		temp_order_obj['sendtype'] = order.consume_type

		# 支付信息
		pay_type_obj = UserPayType.objects.get(id=order.pay_type_id)
		temp_order_obj['paytype'] = pay_type_obj.pay_type
		creditcard_info = {}
		if int(pay_type_obj.pay_type) == 0:
			creditcard_info['cardno'] = pay_type_obj.credit_card
			creditcard_info['pin'] = pay_type_obj.security_code
			creditcard_info['validate_year'] = pay_type_obj.expire_year
			creditcard_info['validate_month'] = pay_type_obj.expire_month
		temp_order_obj['creditcard_info'] = creditcard_info

		# 菜品详情
		dishinfos = []
		for order_dish in order.order_dishes.all():
			temp_dish_obj = {}
			temp_dish_obj['dish_number'] = order_dish.dish_order_number
			temp_dish_obj['dish_name'] = order_dish.dish.name
			temp_dish_obj['dish_type'] = order_dish.dish.dish_type
			temp_dish_obj['dish_price'] = order_dish.dish.price
			sub_dish_list = []
			if int(order_dish.dish.dish_type) == 1:
				for subdish in order_dish.dish.subdishes.all():
					temp_subdish_obj = {}
					temp_subdish_obj['name'] = subdish.name
					temp_subdish_obj['price'] = subdish.price
					sub_dish_list.append(temp_subdish_obj)
			temp_dish_obj['sub_dish_list'] = sub_dish_list
			dishinfos.append(temp_dish_obj)
		temp_order_obj['dishinfos'] = dishinfos

		# 订单价格详情
		price_detail = {}
		price_detail['dish_total_price'] = order.total_price
		price_detail['tax_price'] = order.tax
		price_detail['freight_price'] = order.freight
		price_detail['tip_price'] = order.tip
		temp_order_obj['price_detail'] = price_detail
		order_list.append(temp_order_obj)
	response['orders']['list'] = order_list
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 获取所有已接订单
def get_all_accept_orders(request):
	response = {}
	token = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)
	print shop_obj.name,shop_obj.id
	# 获取已经完成的订单
	orders = Order.objects.filter(shop_id=shop_id,status="ACCEPTED")

	# 分页
	pageno = 1
	pagelength = len(orders)

	if "pageno" in request.GET:
		if int(request.GET['pageno']) > 0:
			pageno = int(request.GET['pageno'])
	if "pagelength" in request.GET:
		pagelength = int(request.GET['pagelength'])

	orders = orders[(pageno-1)*pagelength:pageno*pagelength]
	totol_order_number = len(orders)

	response = {'code':0,'msg':'success'}
	response['orders'] = {}
	response['orders']['count'] = totol_order_number
	order_list = []
	for order in orders:
		temp_order_obj = {}
		temp_order_obj['orderid'] = order.id
		temp_order_obj['order_status'] = 2
		temp_order_obj['ordertime'] = datetime.datetime.strftime(order.create_time,'%Y-%m-%d %H:%M:%S')
		userinfo = {}

		customer = Customer.objects.get(id=order.customer_id) # 获取订单对应用户
		userinfo['name'] = customer.name
		userinfo['phoneno'] = customer.mobile
		temp_order_obj['userinfo'] = userinfo

		# 地址
		delivery_address = DeliveryAddress.objects.get(id=order.delivery_address_id) # 获取订单对应地址信息
		temp_order_obj['orderaddr'] = delivery_address.searched_address + ' ' + delivery_address.detail_address 
		temp_order_obj['sendtype'] = order.consume_type

		# 支付信息
		pay_type_obj = UserPayType.objects.get(id=order.pay_type_id)
		temp_order_obj['paytype'] = pay_type_obj.pay_type
		creditcard_info = {}
		if int(pay_type_obj.pay_type) == 0:
			creditcard_info['cardno'] = pay_type_obj.credit_card
			creditcard_info['pin'] = pay_type_obj.security_code
			creditcard_info['validate_year'] = pay_type_obj.expire_year
			creditcard_info['validate_month'] = pay_type_obj.expire_month
		temp_order_obj['creditcard_info'] = creditcard_info

		# 菜品详情
		dishinfos = []
		for order_dish in order.order_dishes.all():
			temp_dish_obj = {}
			temp_dish_obj['dish_number'] = order_dish.dish_order_number
			temp_dish_obj['dish_name'] = order_dish.dish.name
			temp_dish_obj['dish_type'] = order_dish.dish.dish_type
			temp_dish_obj['dish_price'] = order_dish.dish.price
			sub_dish_list = []
			if int(order_dish.dish.dish_type) == 1:
				for subdish in order_dish.dish.subdishes.all():
					temp_subdish_obj = {}
					temp_subdish_obj['name'] = subdish.name
					temp_subdish_obj['price'] = subdish.price
					sub_dish_list.append(temp_subdish_obj)
			temp_dish_obj['sub_dish_list'] = sub_dish_list
			dishinfos.append(temp_dish_obj)
		temp_order_obj['dishinfos'] = dishinfos

		# 订单价格详情
		price_detail = {}
		price_detail['dish_total_price'] = order.total_price
		price_detail['tax_price'] = order.tax
		price_detail['freight_price'] = order.freight
		price_detail['tip_price'] = order.tip
		temp_order_obj['price_detail'] = price_detail
		order_list.append(temp_order_obj)
	response['orders']['list'] = order_list
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取所有新订单
def get_all_new_orders(request):
	response = {}
	token = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)
	print shop_obj.name,shop_obj.id
	# 获取已经完成的订单
	orders = Order.objects.filter(shop_id=shop_id,status="PROGRESS")
	totol_order_number = len(orders)
	# 分页
	pageno = 1
	pagelength = len(orders)

	if "pageno" in request.GET:
		if int(request.GET['pageno']) > 0:
			pageno = int(request.GET['pageno'])
	if "pagelength" in request.GET:
		pagelength = int(request.GET['pagelength'])

	orders = orders[(pageno-1)*pagelength:pageno*pagelength]
		
	response = {'code':0,'msg':'success'}
	response['orders'] = {}
	response['orders']['count'] = totol_order_number
	order_list = []
	for order in orders:
		temp_order_obj = {}
		temp_order_obj['orderid'] = order.id
		temp_order_obj['order_status'] = 1
		temp_order_obj['ordertime'] = datetime.datetime.strftime(order.create_time,'%Y-%m-%d %H:%M:%S')
		userinfo = {}

		customer = Customer.objects.get(id=order.customer_id) # 获取订单对应用户
		userinfo['name'] = customer.name
		userinfo['phoneno'] = customer.mobile
		temp_order_obj['userinfo'] = userinfo

		# 地址
		delivery_address = DeliveryAddress.objects.get(id=order.delivery_address_id) # 获取订单对应地址信息
		temp_order_obj['orderaddr'] = delivery_address.searched_address + ' ' + delivery_address.detail_address 
		temp_order_obj['sendtype'] = order.consume_type

		# 支付信息
		pay_type_obj = UserPayType.objects.get(id=order.pay_type_id)
		temp_order_obj['paytype'] = pay_type_obj.pay_type
		creditcard_info = {}
		if int(pay_type_obj.pay_type) == 0:
			creditcard_info['cardno'] = pay_type_obj.credit_card
			creditcard_info['pin'] = pay_type_obj.security_code
			creditcard_info['validate_year'] = pay_type_obj.expire_year
			creditcard_info['validate_month'] = pay_type_obj.expire_month
		temp_order_obj['creditcard_info'] = creditcard_info

		# 菜品详情
		dishinfos = []
		for order_dish in order.order_dishes.all():
			temp_dish_obj = {}
			temp_dish_obj['dish_number'] = order_dish.dish_order_number
			temp_dish_obj['dish_name'] = order_dish.dish.name
			temp_dish_obj['dish_type'] = order_dish.dish.dish_type
			temp_dish_obj['dish_price'] = order_dish.dish.price
			sub_dish_list = []
			if int(order_dish.dish.dish_type) == 1:
				for subdish in order_dish.dish.subdishes.all():
					temp_subdish_obj = {}
					temp_subdish_obj['name'] = subdish.name
					temp_subdish_obj['price'] = subdish.price
					sub_dish_list.append(temp_subdish_obj)
			temp_dish_obj['sub_dish_list'] = sub_dish_list
			dishinfos.append(temp_dish_obj)
		temp_order_obj['dishinfos'] = dishinfos

		# 订单价格详情
		price_detail = {}
		price_detail['dish_total_price'] = order.total_price
		price_detail['tax_price'] = order.tax
		price_detail['freight_price'] = order.freight
		price_detail['tip_price'] = order.tip
		temp_order_obj['price_detail'] = price_detail
		order_list.append(temp_order_obj)
	response['orders']['list'] = order_list
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 订单搜索接口
def search_orders(request):
	print "enter search_orders!"
	response = {}
	token = None
	condition = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		
	if 'condition' in request.GET:
		condition = request.GET['condition']
	else:
		code = -100			
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)

	# 满足条件的订单
	orders_by_id = Order.objects.filter(id=condition)
	orders_by_mobile = []
	customers = Customer.objects.filter(mobile=condition)
	print len(customers)
	if len(customers) != 0:
		customer = customers[0]
		orders_by_mobile = Order.objects.filter(customer=customer)
	orders = list(orders_by_id) + list(orders_by_mobile)

	pageno = 1
	pagelength = len(orders)

	if "pageno" in request.GET:
		if int(request.GET['pageno']) > 0:
			pageno = int(request.GET['pageno'])
	if "pagelength" in request.GET:
		pagelength = int(request.GET['pagelength'])
	totol_order_number = len(orders)
	orders = orders[(pageno-1)*pagelength:pageno*pagelength]
	print "order length = ",len(orders)
	response = {'code':0,'msg':'success'}
	response['orders'] = {}
	response['orders']['count'] = totol_order_number
	order_list = []
	for order in orders:
		temp_order_obj = {}
		temp_order_obj['orderid'] = order.id
		if order.status == "PROGRESS":
			temp_order_obj['order_status'] = 1
		elif order.status == "ACCEPTED":
			temp_order_obj['order_status'] = 2
		elif order.status == "SUCCESS":
			temp_order_obj['SUCCESS'] = 3
		elif order.status == "CLOSE":
			temp_order_obj['SUCCESS'] = 4			
		temp_order_obj['ordertime'] = datetime.datetime.strftime(order.create_time,'%Y-%m-%d %H:%M:%S')
		userinfo = {}

		customer = Customer.objects.get(id=order.customer_id) # 获取订单对应用户
		userinfo['name'] = customer.name
		userinfo['phoneno'] = customer.mobile
		temp_order_obj['userinfo'] = userinfo

		# 地址
		delivery_address = DeliveryAddress.objects.get(id=order.delivery_address_id) # 获取订单对应地址信息
		temp_order_obj['orderaddr'] = delivery_address.searched_address + ' ' + delivery_address.detail_address 
		temp_order_obj['sendtype'] = order.consume_type

		# 支付信息
		pay_type_obj = UserPayType.objects.get(id=order.pay_type_id)
		temp_order_obj['paytype'] = pay_type_obj.pay_type
		creditcard_info = {}
		if int(pay_type_obj.pay_type) == 0:
			creditcard_info['cardno'] = pay_type_obj.credit_card
			creditcard_info['pin'] = pay_type_obj.security_code
			creditcard_info['validate_year'] = pay_type_obj.expire_year
			creditcard_info['validate_month'] = pay_type_obj.expire_month
		temp_order_obj['creditcard_info'] = creditcard_info

		# 菜品详情
		dishinfos = []
		for order_dish in order.order_dishes.all():
			temp_dish_obj = {}
			temp_dish_obj['dish_number'] = order_dish.dish_order_number
			temp_dish_obj['dish_name'] = order_dish.dish.name
			temp_dish_obj['dish_type'] = order_dish.dish.dish_type
			temp_dish_obj['dish_price'] = order_dish.dish.price
			sub_dish_list = []
			if int(order_dish.dish.dish_type) == 1:
				for subdish in order_dish.dish.subdishes.all():
					temp_subdish_obj = {}
					temp_subdish_obj['name'] = subdish.name
					temp_subdish_obj['price'] = subdish.price
					sub_dish_list.append(temp_subdish_obj)
			temp_dish_obj['sub_dish_list'] = sub_dish_list
			dishinfos.append(temp_dish_obj)
		temp_order_obj['dishinfos'] = dishinfos

		# 订单价格详情
		price_detail = {}
		price_detail['dish_total_price'] = order.total_price
		price_detail['tax_price'] = order.tax
		price_detail['freight_price'] = order.freight
		price_detail['tip_price'] = order.tip
		temp_order_obj['price_detail'] = price_detail
		order_list.append(temp_order_obj)
	response['orders']['list'] = order_list
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 上传商户地址
def upload_addr(request):
	token = None
	searched_addr = None
	detailed_addr = None
	longitude = None
	latitude = None
	postcode = None
	code = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		

	if 'searched_addr' in request.GET:
		searched_addr = request.GET['searched_addr']
	else:
		code = -100		

	if 'detailed_addr' in request.GET:
		detailed_addr = request.GET['detailed_addr']
	else:
		code = -100		

	if 'longitude' in request.GET:
		longitude = request.GET['longitude']
	else:
		code = -100		

	if 'latitude' in request.GET:
		latitude = request.GET['latitude']
	else:
		code = -100			
		
	if 'postcode' in request.GET:
		postcode = request.GET['postcode']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
											
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)
	shop_obj.search_addr = searched_addr
	shop_obj.detail_addr = detailed_addr
	shop_obj.longitude = float(longitude)
	shop_obj.latitude = float(latitude)
	shop_obj.postcode = postcode
	shop_obj.save()
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

def get_addr(request):
	token = None
	code = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100		

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
											
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	shop_id = (int)(request.session[token])	
	shop_obj = Shop.objects.get(id=shop_id)		
	print shop_id
	response = {'code':0,'msg':'success'}
	response['search_addr'] = shop_obj.search_addr
	response['detail_addr'] = shop_obj.detail_addr
	response['longitude'] = shop_obj.longitude
	response['latitude'] = shop_obj.latitude
	response['postcode'] = shop_obj.postcode
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
# 生成随机字符串
def token_str(randomlength=40):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str