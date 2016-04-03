#coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect
import urllib,urllib2,json,time
from order_dinner.models import Customer,UserPayType,DeliveryAddress,Shop,Dish,Subdish
from random import Random
########################### 
#
#	User Module Interface
#
########################### 

# 用户注册
def register(request):
	response = {}
	## 获取参数
	phoneno = None
	verification_code = None
	password = None
	re_password = None

	code = 0 # 返回代码，默认为0

	# 获取手机号
	if 'phoneno' in request.POST:
		phoneno = request.POST['phoneno']
	else:
		code = -100

	# 获取验证码
	if 'verification_code' in request.POST:
		verification_code = request.POST['verification_code']
	else:
		code = -100

	# 获取密码
	if 'password' in request.POST:
		password = request.POST['password']
	else:
		code = -100

	# 获取再次输入的密码
	if 're_password' in request.POST:
		re_password = request.POST['re_password']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 判断手机是否注册过
	search_users_by_phones = Customer.objects.filter(mobile=phoneno)
	if len(search_users_by_phones) > 0:
		response = {'code':-1,'msg':'phoneno已经注册过'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	print password,re_password
	# 判断密码是否一致
	if password != re_password:
		response = {'code':-2,'msg':'两次输入密码不一致'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 判断验证码是否正确
	if verification_code != '1234': # 暂时写死
		response = {'code':-3,'msg':'验证码错误'} 
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	print '0'
	new_customer = Customer.objects.create(mobile=phoneno,password=password)
	print '1'
	new_customer.save() # 存入数据库
	print "auto saved"
	customer_id = new_customer.id # 用户id
	token = token_str() # 生成token
	request.session[token] = customer_id # 将生成的token记入session中
	response = {'code':0,'msg':'Success','token':token} 
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 用户登录接口
def login(request):
	response = {}
	code = 0 # 返回代码，默认为0
	phoneno = None
	password = None

	# 获取手机号
	if 'phoneno' in request.POST:
		phoneno = request.POST['phoneno']
	else:
		code = -100

	# 获取密码
	if 'password' in request.POST:
		password = request.POST['password']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	search_customers_by_phones = Customer.objects.filter(mobile=phoneno) # 通过手机号搜索用户

	# 如果用户不存在
	if len(search_customers_by_phones) == 0:
		response = {'code':-1,'msg':'用户名不存在'} 
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	searched_customer = search_customers_by_phones[0]
	# 如果密码输入错误
	if searched_customer.password != password:
		response = {'code':-2,'msg':'用户名或密码错误'} 
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	token = token_str() # 生成token
	request.session[token] = searched_customer.id # 将生成的token记入session中
	response = {'code':0,'msg':'Success','token':token} 		
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取用户个人信息
def personal_info(request):
	response = {}
	# 获取参数
	token = None

	code = 0 # 返回代码，默认为0

	# 获取手机号
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	
	# print request.session['test']	
	print 'test' in request.session
	request.session['test'] = 1
	print request.session['test']
	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]
	response = {'code':0,'msg':'success','phoneno':customer.mobile}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 发送手机验证码
def send_verification_code(request):
	response = {}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


########################### 
#
#	User_Pay_Type_Module
#
########################### 

# 新增信用卡接口
def add_credit_card(request):
	response = {}
	## 获取参数
	token = None
	credit_card_no = None
	pin_code = None
	expire_year = None
	expire_month = None

	code = 0 # 返回代码，默认为0

	
	if 'token' in request.POST:
		token = request.POST['token']
	else:
		code = -100	

	if 'credit_card_no' in request.POST:
		credit_card_no = request.POST['credit_card_no']
	else:
		code = -100	

	if 'pin_code' in request.POST:
		pin_code = request.POST['pin_code']
	else:
		code = -100	

	if 'expire_year' in request.POST:
		expire_year = request.POST['expire_year']
	else:
		code = -100	

	if 'expire_month' in request.POST:
		expire_month = request.POST['expire_month']
	else:
		code = -100							

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	# 创建支付方式对象
	user_pay_type = UserPayType.objects.create(pay_type=0,credit_card=credit_card_no,
		security_code=pin_code,expire_year=expire_year,expire_month=expire_month)
	user_pay_type.save()
	customer.customer_user_pay_types.add(user_pay_type) # 为用户添加支付方式
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 用户选取支付方式
def select_paytype(request):
	response = {}
	token = None
	paytype_id = None

	code = 0 # 返回代码，默认为0

	
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if 'paytype_id' in request.GET:
		paytype_id = request.GET['paytype_id']
	else:
		code = -100		
 
 	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看paytype_id是否存在
	paytypes = UserPayType.objects.filter(id=paytype_id) 
	if len(paytypes) == 0:
		response = {'code':-2,'msg':'paytype_id无效'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	customer = customers[0]
	customer.user_pay_type_id = paytypes[0].id
	customer.save()
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取用户支付管理信息
def paytype_infos(request):
	response = {}
	token = None
	code = 0 # 返回代码，默认为0

	
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

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]	

	user_pay_type_objs = customer.userpaytype_set.all()

	response['code'] = 0
	response['msg'] = 'success'
	response['count'] = len(user_pay_type_objs)
	response['paytype_infos'] = []

	for user_pay_type_obj in user_pay_type_objs:
		temp_pay_type_obj = {}
		temp_pay_type_obj['paytype_id'] = user_pay_type_obj.id
		temp_pay_type_obj['type'] = user_pay_type_obj.pay_type
		temp_pay_type_obj['cardno'] = user_pay_type_obj.credit_card
		response['paytype_infos'].append(temp_pay_type_obj)

	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取用户默认支付方式
def get_paytype(request):
	response = {}
	token = None
	code = 0 # 返回代码，默认为0

	
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

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	user_pay_type_id = customer.user_pay_type_id
	if user_pay_type_id == 0:
		response = {'code':-2,'msg':'用户还未指定支付方式'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	user_pay_type_obj = UserPayType.objects.filter(id=user_pay_type_id)[0]
	response['code'] = 0
	response['msg'] = 'success'
	response['pay_type'] = user_pay_type_obj.pay_type
	response['credit_card'] = user_pay_type_obj.credit_card
	response['pin_code'] = user_pay_type_obj.security_code
	response['expire_year'] = user_pay_type_obj.expire_year
	response['expire_month'] = user_pay_type_obj.expire_month

	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

########################### 
#
#	USER ADDRESS MODULE
#
########################### 

# TODO: 等待google服务
# 地点搜索接口
def site_search(request):
	response = {}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 新增收货地址
def add_delivery_address(request):
	response = {}
	token = None
	receiver_name = None
	receiver_phone = None
	searched_address = None
	searched_address_longitude = None
	searched_address_latitude = None
	detail_address = None
	postcode = None
	code = 0 # 返回代码，默认为0

	
	if 'token' in request.POST:
		token = request.POST['token']
	else:
		code = -100	

	if 'receiver_name' in request.POST:
		receiver_name = request.POST['receiver_name']
	else:
		code = -100	

	if 'receiver_phone' in request.POST:
		receiver_phone = request.POST['receiver_phone']
	else:
		code = -100	

	if 'searched_address' in request.POST:
		searched_address = request.POST['searched_address']
	else:
		code = -100	

	if 'searched_address_longitude' in request.POST:
		searched_address_longitude = request.POST['searched_address_longitude']
	else:
		code = -100	

	if 'searched_address_latitude' in request.POST:
		searched_address_latitude = request.POST['searched_address_latitude']
	else:
		code = -100	

	if 'detail_address' in request.POST:
		detail_address = request.POST['detail_address']
	else:
		code = -100	

	if 'postcode' in request.POST:
		postcode = request.POST['postcode']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]
	# 新建DeliveryAddress对象
	delivery_address = DeliveryAddress.objects.create(receiver_name=receiver_name,receiver_phone=receiver_phone,
		searched_address=searched_address,longitude=(float)(searched_address_longitude),latitude=(float)(searched_address_latitude),
		detail_address=detail_address,postcode=postcode)
	delivery_address.save()
	customer.deliveryaddress_set.add(delivery_address)
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 用户选取收货地址
def select_delivery_address(request):
	response = {}
	token = None
	delivery_address_id = None
	code = 0 # 返回代码，默认为0

	
	if 'token' in request.POST:
		token = request.POST['token']
	else:
		code = -100	

	if 'delivery_address_id' in request.POST:
		delivery_address_id = request.POST['delivery_address_id']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	# 查看地址是否有效
	if len(DeliveryAddress.objects.filter(id=delivery_address_id)) == 0:
		response = {'code':-2,'msg':'delivery_address_id无效'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		
	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]
	customer.delivery_address_id = delivery_address_id
	customer.save()
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

# 获取收货地址信息
def delivery_address_infos(request):
	response = {}
	token = None
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

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	response = {'code':0,'msg':'success'}
	response['delivery_address_infos'] = []
	delivery_address_objs = customer.deliveryaddress_set.all()

	for delivery_address_obj in delivery_address_objs:
		temp_delivery_address_obj = {}
		temp_delivery_address_obj['delivery_address_id'] = delivery_address_obj.id
		temp_delivery_address_obj['receiver_name'] = delivery_address_obj.receiver_name
		temp_delivery_address_obj['receiver_phone'] = delivery_address_obj.receiver_phone
		temp_delivery_address_obj['postcode'] = delivery_address_obj.postcode
		temp_delivery_address_obj['address'] = delivery_address_obj.searched_address + ' ' + delivery_address_obj.detail_address
		response['delivery_address_infos'].append(temp_delivery_address_obj)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取用户默认送货地址
def get_user_delivery_address(request):
	response = {}
	token = None
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

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]
	delivery_address_id = customer.delivery_address_id
	delivery_address_objs = DeliveryAddress.objects.filter(id=delivery_address_id)
	response = {'code':0,'msg':'success'}
	if len(delivery_address_objs) != 0:
		delivery_address_obj = delivery_address_objs[0]
		response['delivery_address_id'] = delivery_address_obj.id
		response['username'] = delivery_address_obj.receiver_name
		response['phone'] = delivery_address_obj.receiver_phone
		response['address'] = delivery_address_obj.searched_address + ' ' + delivery_address_obj.detail_address
		response['postcode'] = delivery_address_obj.postcode
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

########################### 
#
#	SHOP MODULE
#
########################### 

# 搜索所有的店铺
def search_shop_infos(request):
	response = {}
	shop_search_term = None
	if 'shop_search_term' in request.GET:
		shop_search_term = request.GET['shop_search_term']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查询shop id
	searched_results = []
	searched_by_id = []
	searched_by_name = []
	searched_by_phone = []
	if shop_search_term.isdigit():
		searched_by_id = Shop.objects.filter(id=(int)(shop_search_term))
	searched_by_name = Shop.objects.filter(name__icontains=shop_search_term)
	searched_by_phone = Shop.objects.filter(mobile__icontains=shop_search_term)
	searched_results = searched_by_id + searched_by_name + searched_by_phone
	response = {'code':0,'msg':'success'}
	response['shop_info_list'] = []
	for searched_result in searched_results:
		temp_searched_result = {}
		temp_searched_result['shop_id'] = searched_result.id
		temp_searched_result['status'] = searched_result.status
		temp_searched_result['img'] = searched_result.shop_img
		temp_searched_result['name'] = searched_result.name
		temp_searched_result['address'] = searched_result.search_addr + ' ' + searched_result.detail_addr
		# TODO :商铺的订单数
		response['shop_info_list'].append(temp_searched_result)
	response = {'code':0,'msg':'success'}		
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取店铺信息详情
def get_shop_detail_info(request):
	response = {}
	shop_id = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# TODO : 订单模块做完
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取所有正在营业中店铺的信息
def get_all_shop_infos(request):
	response = {}
	# TODO : 订单模块做完
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


########################### 
#
#	Dish Module Interface
#
########################### 

# 获取某菜品所有配菜接口
def get_all_side_dishes(request):
	response = {}
	dish_id = None
	if 'dish_id' in request.GET:
		dish_id = request.GET['dish_id']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	# 获取dish_id对应的对象
	dish_objs = Dish.objects.filter(id=dish_id)
	if len(dish_objs) == 0:
		response = {'code':-1,'msg':'dish_id无效'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	dish_obj = dish_objs[0]
	subdish_objs = dish_obj.subdishes
	response = {'code':0,'msg':'success'}
	response['side_dish_info_list'] = []
	for subdish_obj in subdish_objs:
		tmp_subdish_obj = {}
		tmp_subdish_obj['side_dish_id'] = subdish_obj.id
		tmp_subdish_obj['side_dish_name'] = subdish_obj.name
		tmp_subdish_obj['side_dish_price'] = subdish_obj.price
		response['side_dish_info_list'].append(tmp_subdish_obj)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

# 菜品搜索接口
def search_dishes(request):
	response = {}

	shop_id = None
	dish_search_term = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	else:
		code = -100	

	if 'dish_search_term' in request.GET:
		dish_search_term = request.GET['dish_search_term']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	# 获取dish_id对应的对象
	shop_objs = Shop.objects.filter(id=shop_id)
	if len(shop_objs) == 0:
		response = {'code':-1,'msg':'shop_id无效'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	response = {'code':0,'msg':'success'}
	response['dish_info_list'] = []
	dish_objs = Dish.objects.filter(name__icontains=dish_search_term)
	for dish_obj in dish_objs:
		if shop_id == dish_obj.shop.id:
			temp_dish_obj = {}
			temp_dish_obj['dish_id'] = dish_obj.id
			temp_dish_obj['dish_type'] = dish_obj.dish_type
			temp_dish_obj['dish_img'] = dish_obj.dish_img
			temp_dish_obj['dish_name'] = dish_obj.name
			# TODO 订单数
			temp_dish_obj['dish_price'] = dish_obj.price
			response['dish_info_list'].append(temp_dish_obj)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

########################### 
#
#	Order Module Interface
#
########################### 

# 用户提交订单
def upload_order(request):
	response = {}
	# 获取参数
	token = None
	shop_id = None
	delivery_address_id = None
	code = 0 # 返回代码，默认为0

	# 获取手机号
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

	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
# 生成随机字符串
def token_str(randomlength=12):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str