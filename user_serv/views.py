#coding=utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
import urllib,urllib2,json,time,datetime
from order_dinner.models import Customer,UserPayType,DeliveryAddress,Shop,Dish,Subdish,VerificationCode,Order,OrderDish,OrderSubDish,BannerImg,GlobalSetting
from random import Random
from django.contrib import auth
import sms_sender
import jpush
# from bs4 import BeautifulSoup

########################### 
#
#	User Module Interface
#
########################### 

# 用户注册
# @csrf_exempt
def register(request):
	response = {}
	## 获取参数
	phoneno = None
	verification_code = None
	password = None
	re_password = None

	code = 0 # 返回代码，默认为0

	# 获取手机号
	if 'phoneno' in request.GET:
		phoneno = request.GET['phoneno']
	else:
		code = -100

	# 获取验证码
	if 'verification_code' in request.GET:
		verification_code = request.GET['verification_code']
	else:
		code = -100

	# 获取密码
	if 'password' in request.GET:
		password = request.GET['password']
	else:
		code = -100

	# 获取再次输入的密码
	if 're_password' in request.GET:
		re_password = request.GET['re_password']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 判断手机是否注册过
	search_users_by_phones = Customer.objects.filter(mobile=phoneno)
	if len(search_users_by_phones) > 0:
		response = {'code':-1,'msg':'手机号已经注册过','msg_en':'The phone number is already registered'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	print password,re_password
	# 判断密码是否一致
	if password != re_password:
		response = {'code':-2,'msg':'两次输入密码不一致','msg_en':'The passwords twice entered are inconsistent'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 判断验证码是否正确
	verification_code_objs = VerificationCode.objects.filter(mobile="+1"+phoneno)
	print len(verification_code_objs)
	if len(verification_code_objs) == 0:
		response = {'code':-3,'msg':'验证码错误','msg_en':'Verification code error'} 
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	else:
		verification_code_record = verification_code_objs[0].verification_code
		print verification_code_record,verification_code
		if str(verification_code_record) != verification_code:
			response = {'code':-3,'msg':'验证码错误','msg_en':'Verification code error'} 
			return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))			

	new_customer = Customer.objects.create(mobile=phoneno,password=password)
	new_customer.save() # 存入数据库
	customer_id = new_customer.id # 用户id
	token = token_str() # 生成token
	request.session[token] = customer_id # 将生成的token记入session中
	response = {'code':0,'msg':'Success','token':token} 
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 用户登录接口
@csrf_exempt
def login(request):
	response = {}
	code = 0 # 返回代码，默认为0
	phoneno = None
	password = None

	# 获取手机号
	if 'phoneno' in request.GET:
		phoneno = request.GET['phoneno']
	else:
		code = -100

	# 获取密码
	if 'password' in request.GET:
		password = request.GET['password']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	search_customers_by_phones = Customer.objects.filter(mobile=phoneno) # 通过手机号搜索用户

	# 如果用户不存在
	if len(search_customers_by_phones) == 0:
		response = {'code':-1,'msg':'用户名不存在','msg_en':'User does not exist'} 
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	searched_customer = search_customers_by_phones[0]
	# 如果密码输入错误
	if searched_customer.password != password:
		response = {'code':-2,'msg':'用户名或密码错误','msg_en':'Wrong username or password'} 
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

	# 获取token
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]
	response = {'code':0,'msg':'success','phoneno':customer.mobile}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 发送手机验证码
def send_verification_code(request):
	response = {}
	# 获取参数
	phoneno = None
	code = None

	# 获取手机号
	if 'phoneno' in request.GET:
		phoneno = request.GET['phoneno']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	verification_code = sms_sender.token_str()
	phoneno = "+1"+phoneno
	response_str = sms_sender.jindouyun_sms_sender(phoneno,verification_code)
	# 将短信验证码记录
	verification_code_records = VerificationCode.objects.filter(mobile=phoneno)
	verification_code_obj = None
	if len(verification_code_records) == 0:
		verification_code_obj = VerificationCode.objects.create(mobile=phoneno,verification_code=verification_code)
		verification_code_obj.save()
	else:
		verification_code_obj = verification_code_records[0]
		verification_code_obj.verification_code = verification_code
		verification_code_obj.save()
	print response_str
	print type(response_str)
	response_dict = json.loads(response_str)
	response['code'] = (int)(response_dict['code'])
	response['msg'] = response_dict['msg']
	if int(response['code']) == 0:
		response['verification_code'] = verification_code
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

	
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if 'credit_card_no' in request.GET:
		credit_card_no = request.GET['credit_card_no']
	else:
		code = -100	

	if 'pin_code' in request.GET:
		pin_code = request.GET['pin_code']
	else:
		code = -100	

	if 'expire_year' in request.GET:
		expire_year = request.GET['expire_year']
	else:
		code = -100	

	if 'expire_month' in request.GET:
		expire_month = request.GET['expire_month']
	else:
		code = -100							
	print credit_card_no,pin_code,expire_year,expire_month
	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	# 创建支付方式对象
	user_pay_type = UserPayType.objects.create(customer=customer,pay_type=0,credit_card=credit_card_no,
		security_code=pin_code,expire_year=expire_year,expire_month=expire_month)
	user_pay_type.save()
	# customer.customer_user_pay_types.add(user_pay_type) # 为用户添加支付方式
	response = {'code':0,'msg':'success',"pay_type_id":user_pay_type.id}
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
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！' ,'msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看paytype_id是否存在
	paytypes = UserPayType.objects.filter(id=paytype_id) 
	if len(paytypes) == 0:
		response = {'code':-2,'msg':'paytype_id无效','msg_en':'paytype_id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	customer = customers[0]
	customer.user_pay_type_id = paytypes[0].id
	customer.save()
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 删除支付方式
def delete_paytype(request):
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
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！' ,'msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	customer = customers[0]

	# 查看paytype_id是否存在
	paytypes = UserPayType.objects.filter(id=paytype_id,customer=customer) 
	if len(paytypes) == 0:
		response = {'code':-2,'msg':'paytype_id无效','msg_en':'paytype_id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		
	paytypes[0].delete()


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
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！' ,'msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]	

	user_pay_type_objs = UserPayType.objects.filter(customer_id=customer.id)
	user_pay_type_no_cards = UserPayType.objects.filter(pay_type=1) # 货到付款
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
	for user_pay_type_no_card in user_pay_type_no_cards:
		temp_pay_type_obj = {}
		temp_pay_type_obj['paytype_id'] = user_pay_type_no_card.id
		temp_pay_type_obj['type'] = user_pay_type_no_card.pay_type
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
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！' ,'msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	user_pay_type_id = customer.user_pay_type_id
	if user_pay_type_id == 0:
		response = {'code':-2,'msg':'用户还未指定支付方式' ,'msg_en':'Choose pay type first!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	user_pay_type_obj = UserPayType.objects.filter(id=user_pay_type_id)[0]
	response['code'] = 0
	response['msg'] = 'success'
	response['paytype_id'] = user_pay_type_obj.id
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

# 地点搜索接口
def site_search(request):
	response = {}
	address = None
	code = 0 # 返回代码，默认为0

	if 'address' in request.GET:
		address = request.GET['address']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	params = urllib.urlencode({'query': address, 'key': 'AIzaSyAcqwDjEnYPte9qNnCEH3L12doj8fZRnEY'})
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?%s" % params
	print url
	f = urllib.urlopen(url)
	response_str = f.read().decode('utf-8')
	response_dict = json.loads(response_str)
	response = {'code':0,'msg':'success'}
	print response_dict
	print type(response_dict)
	results = response_dict['results']
	response['address_list'] = []
	for result in results:
		temp_resut = {}
		temp_resut['place_id'] = result['id']
		temp_resut['detail_address'] = result['formatted_address'] + ' ' + result['name']
		temp_resut['longitude'] = result['geometry']['location']['lng']
		temp_resut['latitude'] = result['geometry']['location']['lat']
		response['address_list'].append(temp_resut)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 临时删除用户
def drop_user(request):
	response = {}
	mobile = None
	code = 0 # 返回代码，默认为0

	if 'mobile' in request.GET:
		mobile = request.GET['mobile']
	else:
		code = -100

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	customers = Customer.objects.filter(mobile=mobile)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]
	customer.delete()
	response = {'code':0,'msg':'success'}
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

	
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if 'receiver_name' in request.GET:
		receiver_name = request.GET['receiver_name']
	else:
		code = -100	

	if 'receiver_phone' in request.GET:
		receiver_phone = request.GET['receiver_phone']
	else:
		code = -100	

	if 'searched_address' in request.GET:
		searched_address = request.GET['searched_address']
	else:
		code = -100	

	if 'searched_address_longitude' in request.GET:
		searched_address_longitude = request.GET['searched_address_longitude']
	else:
		code = -100	

	if 'searched_address_latitude' in request.GET:
		searched_address_latitude = request.GET['searched_address_latitude']
	else:
		code = -100	

	if 'detail_address' in request.GET:
		detail_address = request.GET['detail_address']
	else:
		code = -100	

	if 'postcode' in request.GET:
		postcode = request.GET['postcode']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！' ,'msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]
	# 新建DeliveryAddress对象
	delivery_address = DeliveryAddress.objects.create(customer=customer,receiver_name=receiver_name,receiver_phone=receiver_phone,
		searched_address=searched_address,longitude=(float)(searched_address_longitude),latitude=(float)(searched_address_latitude),
		detail_address=detail_address,postcode=postcode)
	delivery_address.save()
	# customer.deliveryaddress_set.add(delivery_address) 
	response = {'code':0,'msg':'success',"delivery_address_id":delivery_address.id}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 用户选取收货地址
def select_delivery_address(request):
	response = {}
	token = None
	delivery_address_id = None
	code = 0 # 返回代码，默认为0

	
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if 'delivery_address_id' in request.GET:
		delivery_address_id = request.GET['delivery_address_id']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！' ,'msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	# 查看地址是否有效
	if len(DeliveryAddress.objects.filter(id=delivery_address_id)) == 0:
		response = {'code':-2,'msg':'delivery_address_id无效','msg_en':'Delivery Address Invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		
	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
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
	code = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	response = {'code':0,'msg':'success'}
	response['delivery_address_infos'] = []
	delivery_address_objs = DeliveryAddress.objects.filter(customer_id=customer.id)

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
	code = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
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

# 删除收货地址
def delete_delivery_address(request):
	response = {}
	delivery_address_id = None
	token = None
	code = None
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	

	if 'delivery_address_id' in request.GET:
		delivery_address_id = request.GET['delivery_address_id']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	
	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	# 获取地址对象
	delivery_address_objs = DeliveryAddress.objects.filter(id=delivery_address_id,customer=customer)
	if len(delivery_address_objs) == 0:
		response = {'code':-2,'msg':'delivery_address_id无效','msg_en':'Delivery Address Invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	delivery_address_obj = delivery_address_objs[0]
	delivery_address_obj.delete()
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 编辑地址对象
def edit_delivery_address(request):
	response = {}
	
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
	code = None
	if 'shop_search_term' in request.GET:
		shop_search_term = request.GET['shop_search_term']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	# 查询shop id
	searched_results = []
	searched_by_id = []
	searched_by_name = []
	searched_by_phone = []
	searched_by_name_en = []
	if shop_search_term.isdigit():
		searched_by_id = Shop.objects.filter(id=(int)(shop_search_term))
	searched_by_name = Shop.objects.filter(name__icontains=shop_search_term)
	searched_by_phone = Shop.objects.filter(mobile__icontains=shop_search_term)
	searched_by_name_en = Shop.objects.filter(name_en__icontains=shop_search_term)
	searched_results = list(searched_by_id) + list(searched_by_name) + list(searched_by_phone) + list(searched_by_name_en)
	response = {'code':0,'msg':'success'}
	response['shop_info_list'] = []
	now = datetime.datetime.now()
	month = now.month
	year = now.year
	for searched_result in searched_results:
		temp_searched_result = {}
		temp_searched_result['shop_id'] = searched_result.id
		temp_searched_result['status'] = searched_result.status
		temp_searched_result['img'] = "http://resource.jindouyunonline.com:8001/media/" + searched_result.shop_img.name
		temp_searched_result['name_en'] = searched_result.name_en
		temp_searched_result['name_cn'] = searched_result.name
		temp_searched_result['shop_feature'] = searched_result.shop_feature
		temp_searched_result['shop_feature_en'] = searched_result.shop_feature_en
		temp_searched_result['address'] = searched_result.search_addr + ' ' + searched_result.detail_addr
		start_date = datetime.date(year,month,1)
		end_date = None
		if month == 12:
			end_date = datetime.date(year+1,1,1)
		else:
			end_date = datetime.date(year,month+1,1)
		current_month_orders = Order.objects.filter(shop_id=searched_result.id).filter(create_time__range=(start_date,end_date))
		temp_searched_result['current_month_order'] = len(current_month_orders)
		response['shop_info_list'].append(temp_searched_result)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取店铺信息详情
def get_shop_detail_info(request):
	response = {}
	shop_id = None

	code = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_objs = Shop.objects.filter(id=shop_id)
	if len(shop_objs) == 0:
		response = {'code':-1,'msg':'shop_id无效','msg_en':'shop id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	
	shop = shop_objs[0]
	response = {'code':0,'msg':'success'}
	response['status'] = shop.status
	response['shop_img'] = "http://resource.jindouyunonline.com:8001/media/" + shop.shop_img.name
	response['name_cn'] = shop.name
	response['name_en'] = shop.name_en
	response['shop_feature'] = shop.shop_feature
	response['shop_feature_en'] = shop.shop_feature_en
	response['dish_info_list'] = []
	response['shop_detail_info'] = {}
	response['shop_detail_info']['address'] = shop.search_addr + ' ' + shop.detail_addr
	response['shop_detail_info']['phone'] = shop.mobile
	response['shop_detail_info']['delivery_time'] = shop.business_hour
	dishes = Dish.objects.filter(shop=shop)
	now = datetime.datetime.now()
	month = now.month
	year = now.year	
	for dish in dishes:
		temp_dish_info = {}
		temp_dish_info['dish_id'] = dish.id
		temp_dish_info['dish_type'] = dish.dish_type
		temp_dish_info['dish_name_cn'] = dish.name
		temp_dish_info['dish_name_en'] = dish.name_en
		temp_dish_info['dish_img'] = "http://resource.jindouyunonline.com:8001/media/" + dish.dish_img.name
		temp_dish_info['dish_price'] = dish.price
		temp_dish_info['current_month_order'] = 0
		start_date = datetime.date(year,month,1)
		end_date = None
		if month == 12:
			end_date = datetime.date(year+1,1,1)
		else:
			end_date = datetime.date(year,month+1,1)
		current_month_shop_orders = Order.objects.filter(shop_id=shop.id).filter(create_time__range=(start_date,end_date))
		for current_month_shop_order in current_month_shop_orders:
			for order_dish in current_month_shop_order.order_dishes.all():
				if order_dish.dish.id == dish.id:
					temp_dish_info['current_month_order'] += 1
		response['dish_info_list'].append(temp_dish_info)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取所有正在营业中店铺的信息
def get_all_shop_infos(request):
	response = {}
	response = {'code':0,'msg':'success'}
	response['shop_info_list'] = []
	
	now = datetime.datetime.now()
	month = now.month
	year = now.year
	shops = Shop.objects.all()

	total_shop_number = len(shops)
	response['total_shop_number'] = total_shop_number
	pageno = 1
	pagelength = len(shops)
	if "pageno" in request.GET:
		if int(request.GET['pageno']) > 0:
			pageno = int(request.GET['pageno'])
	if "pagelength" in request.GET:
		pagelength = int(request.GET['pagelength'])
	
	shops = shops[(pageno-1)*pagelength:pageno*pagelength]
	for shop in shops:
		temp_shop_obj = {}
		temp_shop_obj['status'] = shop.status
		temp_shop_obj['shop_id'] = shop.id
		temp_shop_obj['img'] = "http://resource.jindouyunonline.com:8001/media/" + shop.shop_img.name
		temp_shop_obj['name_cn'] = shop.name
		temp_shop_obj['name_en'] = shop.name_en
		temp_shop_obj['shop_feature'] = shop.shop_feature
		temp_shop_obj['shop_feature_en'] = shop.shop_feature_en
		temp_shop_obj['address'] = shop.search_addr + ' ' + shop.detail_addr
		start_date = datetime.date(year,month,1)
		end_date = None
		if month == 12:
			end_date = datetime.date(year+1,1,1)
		else:
			end_date = datetime.date(year,month+1,1)
		current_month_shop_orders = Order.objects.filter(shop_id=shop.id).filter(create_time__range=(start_date,end_date))	
		temp_shop_obj['current_month_order'] = len(current_month_shop_orders)
		response['shop_info_list'].append(temp_shop_obj)
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
	code = None
	if 'dish_id' in request.GET:
		dish_id = request.GET['dish_id']
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	# 获取dish_id对应的对象
	dish_objs = Dish.objects.filter(id=dish_id)
	if len(dish_objs) == 0:
		response = {'code':-1,'msg':'dish_id无效','msg_en':'dish id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	dish_obj = dish_objs[0]
	subdish_objs = dish_obj.subdishes.all()
	response = {'code':0,'msg':'success'}
	response['side_dish_info_list'] = []
	for subdish_obj in subdish_objs:
		tmp_subdish_obj = {}
		tmp_subdish_obj['side_dish_id'] = subdish_obj.id
		tmp_subdish_obj['side_dish_cn_name'] = subdish_obj.name
		tmp_subdish_obj['side_dish_en_name'] = subdish_obj.name_en
		tmp_subdish_obj['side_dish_price'] = subdish_obj.price
		response['side_dish_info_list'].append(tmp_subdish_obj)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

# 菜品搜索接口
def search_dishes(request):
	response = {}
	shop_id = None
	dish_search_term = None
	code = None
	if 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']
	else:
		code = -100	

	if 'dish_search_term' in request.GET:
		dish_search_term = request.GET['dish_search_term']
	else:
		code = -100	

	
	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	# 获取dish_id对应的对象
	shop_objs = Shop.objects.filter(id=shop_id)
	if len(shop_objs) == 0:
		response = {'code':-1,'msg':'shop_id无效','msg_en':'shop id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	response = {'code':0,'msg':'success'}
	response['dish_info_list'] = []
	dish_objs = Dish.objects.filter(name__icontains=dish_search_term) | Dish.objects.filter(name_en__icontains=dish_search_term)
	now = datetime.datetime.now()
	month = now.month
	year = now.year
	for dish_obj in dish_objs:
		print shop_id,dish_obj.shop.id,shop_id==dish_obj.shop.id
		if int(shop_id) == int(dish_obj.shop.id):
			temp_dish_obj = {}
			temp_dish_obj['dish_id'] = dish_obj.id
			temp_dish_obj['dish_type'] = dish_obj.dish_type
			temp_dish_obj['dish_img'] = "http://resource.jindouyunonline.com:8001/media/" + dish_obj.dish_img.name
			temp_dish_obj['dish_cn_name'] = dish_obj.name
			temp_dish_obj['dish_en_name'] = dish_obj.name_en
			start_date = datetime.date(year,month,1)
			end_date = None
			if month == 12:
				end_date = datetime.date(year+1,1,1)
			else:
				end_date = datetime.date(year,month+1,1)
			current_month_orders = Order.objects.filter(shop_id=shop_id).filter(create_time__range=(start_date,end_date))
			current_month_order_number = 0
			for current_month_order in current_month_orders:
				for order_dish in current_month_order.order_dishes.all():
					if int(dish_obj.id) == int(order_dish.dish.id):
						current_month_order_number += 1
			temp_dish_obj['current_month_order'] = current_month_order_number
			temp_dish_obj['dish_price'] = dish_obj.price
			print temp_dish_obj
			response['dish_info_list'].append(temp_dish_obj)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取详情
def get_dish_detail(request):
	response = {}
	dish_id = None
	code = None
	if 'dish_id' in request.GET:
		dish_id = request.GET['dish_id']
	else:
		code = -100	
	
	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	dishes = Dish.objects.filter(id=dish_id)
	if len(dishes) == 0:
		response = {'code':-1,'msg':'dish_id无效','msg_en':'dish id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		
	dish = dishes[0]
	temp_dish_info = {}
	temp_dish_info = {'code':0,'msg':'success'}
	temp_dish_info['dish_id'] = dish.id
	temp_dish_info['dish_type'] = dish.dish_type
	temp_dish_info['dish_name_cn'] = dish.name
	temp_dish_info['dish_name_en'] = dish.name_en
	temp_dish_info['dish_img'] = "http://resource.jindouyunonline.com:8001/media/" + dish.dish_img.name
	temp_dish_info['dish_price'] = dish.price
	temp_dish_info['current_month_order'] = 0
	now = datetime.datetime.now()
	month = now.month
	year = now.year
	start_date = datetime.date(year,month,1)
	end_date = None

	if month == 12:
		end_date = datetime.date(year+1,1,1)
	else:
		end_date = datetime.date(year,month+1,1)
	shop = dish.shop
	current_month_shop_orders = Order.objects.filter(shop_id=shop.id).filter(create_time__range=(start_date,end_date))
	for current_month_shop_order in current_month_shop_orders:
		for order_dish in current_month_shop_order.order_dishes.all():
			if order_dish.dish.id == dish.id:
				temp_dish_info['current_month_order'] += 1	
	response = temp_dish_info
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
########################### 
#
#	Order Module Interface
#
########################### 

# 用户提交订单
@csrf_exempt
def upload_order(request):
	response = {}
	# 获取参数
	token = None
	shop_id = None
	delivery_address_id = None
	paytype_id = None
	consume_type = None
	tip_type = None
	tip_ratio = None
	remark = None
	freight = None
	distance = None
	tax = None
	dish_order_list = None # list参数
	code = 0 # 返回代码，默认为0

	# 获取token
	if 'token' in request.POST:
		token = request.POST['token']
	elif 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100	
	
	# 获取shop_id
	if 'shop_id' in request.POST:
		shop_id = request.POST['shop_id']
	elif 'shop_id' in request.GET:
		shop_id = request.GET['shop_id']		
	else:
		code = -100	

	# 获取delivery_address_id
	if 'delivery_address_id' in request.POST:
		delivery_address_id = request.POST['delivery_address_id']
	elif 'delivery_address_id' in request.GET:
		delivery_address_id = request.GET['delivery_address_id']			
	else:
		code = -100	

	# 获取paytype_id
	if 'paytype_id' in request.POST:
		paytype_id = request.POST['paytype_id']
	elif 'paytype_id' in request.GET:
		paytype_id = request.GET['paytype_id']			
	else:
		code = -100	

	# 获取consume_type
	if 'consume_type' in request.POST:
		consume_type = request.POST['consume_type']
	elif 'consume_type' in request.GET:
		consume_type = request.GET['consume_type']			
	else:
		code = -100		

	# 获取tip_type
	if 'tip_type' in request.POST:
		tip_type = request.POST['tip_type']
	elif 'tip_type' in request.GET:
		tip_type = request.GET['tip_type']			
	else:
		code = -100		

	# 获取tip_ratio
	if 'tip_ratio' in request.POST:
		tip_ratio = request.POST['tip_ratio']
	elif 'tip_ratio' in request.GET:
		tip_ratio = request.GET['tip_ratio']			
	else:
		code = -100	

	# 获取remark
	if 'remark' in request.POST:
		remark = request.POST['remark']
	elif 'remark' in request.GET:
		remark = request.GET['remark']				
	else:
		code = -100		


	# 获取distance
	if 'distance' in request.POST:
		distance = request.POST['distance']
	elif 'distance' in request.GET:
		distance = request.GET['distance']			
	else:
		code = -100	

	# 获取dish_order_list
	if 'dish_order_list' in request.POST:
		dish_order_list = request.POST['dish_order_list']
	elif 'dish_order_list' in request.GET:
		dish_order_list = request.GET['dish_order_list']					
	else:
		code = -100	

	print token,shop_id,delivery_address_id,paytype_id,consume_type,tip_type,tip_ratio,remark,freight,distance,tax,dish_order_list

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		


	# 获取shop_id对应的对象
	shop_objs = Shop.objects.filter(id=shop_id)
	if len(shop_objs) == 0:
		response = {'code':-2,'msg':'shop_id无效','msg_en':'shop id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	
	shop_obj = shop_objs[0]

	# 查看地址是否有效
	if len(DeliveryAddress.objects.filter(id=delivery_address_id)) == 0:
		response = {'code':-3,'msg':'delivery_address_id无效','msg_en':'delivery address invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	delivery_address_obj = DeliveryAddress.objects.get(id=delivery_address_id)

	# 查看paytype_id是否存在
	paytypes = UserPayType.objects.filter(id=paytype_id) 
	if len(paytypes) == 0:
		response = {'code':-4,'msg':'paytype_id无效','msg_en':'pay type id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	
	paytype_obj = paytypes[0]
	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	# 新建订单对象
	new_order = Order.objects.create(customer=customer,shop=shop_obj,tip_type=tip_type,
		distance=distance,remark=remark,status="PROGRESS",delivery_address=delivery_address_obj,
		pay_type=paytype_obj,consume_type=consume_type)
	new_order.save()

	# 为此订单添加菜品记录
	dish_order_list = dish_order_list.replace("'","\"")
	dish_order_list = dish_order_list.replace('u\"',"\"")
	dish_order_list = json.loads(dish_order_list)

	global_set = GlobalSetting.objects.all()[0]

	total_dish_price = 0 # 所点菜品总价格
	for dish_order in dish_order_list:
		dish_id = int(dish_order['dish_id'])
		order_number = int(dish_order['order_number'])
		dish_obj = Dish.objects.get(id=dish_id)
		dish_type = int(dish_obj.dish_type) # 菜品类型
		order_dish_obj = OrderDish.objects.create(dish=dish_obj,dish_order_number=order_number) # 新建订单中的菜品对象
		order_dish_obj.save()
		if dish_type == 1: # 含有配菜的菜品
			for side_dish in dish_order['side_dish_list']:
				side_dish_id = side_dish['side_dish_id']
				side_dish_order_number = side_dish['order_number']
				subdish_obj = Subdish.objects.get(id=side_dish_id)
				total_dish_price += float(side_dish_order_number) * float(subdish_obj.price) # 价格加总
				order_subdish_obj = OrderSubDish.objects.create(subdish=subdish_obj,subdish_order_number=side_dish_order_number)
				order_subdish_obj.save()
				order_dish_obj.ordered_subdishes.add(order_subdish_obj) # 添加子菜品
				order_dish_obj.save()
		else:
			total_dish_price += float(order_number) * float(dish_obj.price) # 价格加总
		new_order.order_dishes.add(order_dish_obj) # 订单添加菜品
		new_order.save()
	print '总价格',total_dish_price

	# 额外费用
	# 运费
	print "distance= ",distance
	freight_price = 0
	if float(total_dish_price) < global_set.freight_thres:
		freight_price = float("%.1f" % (float(distance) / (float)(1.6)))
	# 佣金
	commission = float("%.1f" %(float(total_dish_price) * float(shop_obj.commission)))
	# 小费
	tip = 0
	if tip_type == 0:
		tip = float("%.1f" %(float(tip_ratio) * float(total_dish_price)))
	print tip_ratio,tip
	# 税
	tax = float("%.1f" %(float(total_dish_price) * float(global_set.tax_rate)))
	print tax
	# 折扣
	discount_price = float("%.1f" %(float(total_dish_price) * float(global_set.discount_rate)))
	print global_set.tax_rate,discount_price
	# 最终应付价格
	payable_price = total_dish_price + freight_price + tip + tax - discount_price
	new_order.origin_price = total_dish_price
	new_order.freight = freight_price
	new_order.commission_price = commission
	new_order.tip = tip
	new_order.tax = tax
	new_order.discount_price = discount_price
	new_order.total_price = payable_price
	new_order.save()

	# 极光推送消息
	APP_KEY="d574d8f5f6fc8933599e4683"
	MASTER_SECRET="804fe51a04d44ae35610a25b"
	_jpush = jpush.JPush(APP_KEY, MASTER_SECRET)	
	push = _jpush.create_push()
	push.audience = jpush.audience(jpush.registration_id(shop_obj.registration_id))
	alert_msg = "您有新订单!手机号: %s下单" % customer.mobile
	push.notification = jpush.notification(alert=alert_msg)
	push.options = {"time_to_live":86400, "sendno":12345,"apns_production":True}
	push.platform = jpush.all_
	push.send()
	# 极光推送消息结束
	response = {'code':0,'msg':'success'}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取用户所有的订单信息
def get_all_orders(request):
	response = {}
	token = None
	code = 0 # 返回代码，默认为0

	# 获取token
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		
	print token
	print request.session[token]
	global_set = GlobalSetting.objects.all()[0]
	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]

	orders = Order.objects.filter(customer=customer)
	response = {'code':0,'msg':'success'}
	response['order_list'] = []
	for order in orders:
		temp_order_obj = {}
		temp_order_obj['order_id'] = order.id
		temp_order_obj['order_status'] = order.status
		temp_order_obj['shop_cn_name'] = order.shop.name
		temp_order_obj['shop_en_name'] = order.shop.name_en
		temp_order_obj['shop_img'] = "http://resource.jindouyunonline.com:8001/media/" + order.shop.shop_img.name
		temp_order_obj['total_price'] = order.total_price
		temp_order_obj['discount_rate'] = global_set.discount_rate
		temp_order_obj['dish_price'] = order.origin_price #菜品总价
		temp_order_obj['payable_price'] = order.total_price #应付价格
		temp_order_obj['order_create_time'] = datetime.datetime.strftime(order.create_time,'%Y-%m-%d %H:%M:%S')
		response['order_list'].append(temp_order_obj)

	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取订单详情信息
def get_order_detail_info(request):
	response = {}
	token = None
	order_id = None
	code = 0 # 返回代码，默认为0

	# 获取token
	if 'token' in request.GET:
		token = request.GET['token']
	else:
		code = -100

	# 获取orderid
	if 'order_id' in request.GET:
		order_id = int(request.GET['order_id'])
	else:
		code = -100

	# 查看token是否存在session中
	if token not in request.session:
		response = {'code':-1,'msg':'token失效，需重新登录','msg_en':'Need to re-login'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

	global_set = GlobalSetting.objects.all()[0]

	# 获取token对应的用户
	customer_id = request.session[token]
	customers = Customer.objects.filter(id=customer_id)
	if len(customers) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	customer = customers[0]	

	# 获取订单对象
	orders = Order.objects.filter(id=order_id)
	if len(orders) == 0:
		response = {'code':-200,'msg':'其他错误','msg_en':'Other Failure'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	order = orders[0]
	response = {'code':0,'msg':'success'}
	response['delivery_address_id'] = order.delivery_address.id
	response['paytype_id'] = order.pay_type.id
	response['consume_type'] = order.consume_type
	response['tip_type'] = order.tip_type
	response['tip'] = order.tip
	response['remark'] = order.remark
	response['freight'] = order.freight
	response['distance'] = order.distance
	response['tax'] = order.tax
	response['discount_rate'] = global_set.discount_rate
	response['dish_price'] = order.origin_price
	response['payable_price'] = order.total_price
	response['order_create_time'] = datetime.datetime.strftime(order.create_time,'%Y-%m-%d %H:%M:%S')
	response['dish_order_list'] = []
	for order_dish in order.order_dishes.all():
		temp_dish_obj = {}
		temp_dish_obj['dish_id'] = order_dish.dish.id
		temp_dish_obj['dish_type'] = order_dish.dish.dish_type
		temp_dish_obj['order_number'] = order_dish.dish_order_number
		temp_dish_obj['dish_name_cn'] = order_dish.dish.name
		temp_dish_obj['dish_name_en'] = order_dish.dish.name_en
		temp_dish_obj['dish_price'] = order_dish.dish.price
		if int(temp_dish_obj['dish_type']) == 1:
			temp_dish_obj['side_dish_list'] = []
			temp_dish_price = 0.0
			for ordered_subdish in order_dish.ordered_subdishes.all():
				temp_subdish_obj = {}
				temp_subdish_obj['side_dish_id'] = ordered_subdish.subdish.id
				temp_subdish_obj['order_number'] = ordered_subdish.subdish_order_number
				temp_subdish_obj['side_dish_name_cn'] = ordered_subdish.subdish.name
				temp_subdish_obj['side_dish_name_en'] = ordered_subdish.subdish.name_en
				temp_subdish_obj['side_dish_price'] = ordered_subdish.subdish.price
				temp_dish_price += float(ordered_subdish.subdish_order_number) * float(ordered_subdish.subdish.price)
				temp_dish_obj['side_dish_list'].append(temp_subdish_obj)
			temp_dish_obj['dish_price'] = temp_dish_price
		response['dish_order_list'].append(temp_dish_obj)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 计算用户到商家的距离
def calculate_distance(request):
	shop_id = None
	delivery_address_id = None
	code = None
	# 获取shop_id
	if 'shop_id' in request.GET:
		shop_id = int(request.GET['shop_id'])
	else:
		code = -100	

	if 'delivery_address_id' in request.GET:
		delivery_address_id = int(request.GET['delivery_address_id'])
	else:
		code = -100	

	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	shop_objs = Shop.objects.filter(id=int(shop_id))
	if len(shop_objs) == 0:
		response = {'code':-1,'msg':'shop_id无效','msg_en':'shop id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	shop = shop_objs[0]

	delivery_address_objs = DeliveryAddress.objects.filter(id=int(delivery_address_id))	
	if len(delivery_address_objs) == 0:
		response = {'code':-2,'msg':'delivery_address_id无效','msg_en':'delivery address id invalid'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
	delivery_address = delivery_address_objs[0]

	if shop.longitude == None or shop.latitude == None or shop.longitude == 0.0 or shop.latitude == 0.0:
		response = {'code':-3,'msg':'商户尚没有上传地址','msg_en':'The shop has not uploaded address yet!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

	origin_addr = "%f,%f" % (delivery_address.latitude,delivery_address.longitude)
	dest_addr = "%f,%f" % (shop.latitude,shop.longitude)
	params = urllib.urlencode({'origins': origin_addr,"destinations":dest_addr,'key': 'AIzaSyAcqwDjEnYPte9qNnCEH3L12doj8fZRnEY',"language":"en"})
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?%s" % params
	print url
	f = urllib.urlopen(url)
	response_str = f.read().decode('utf-8')
	response_dict = json.loads(response_str)
	distance = 0
	try:
		if response_dict["status"] != "OK":
			response = {'code':-4,'msg':'收货地址无法计算距离，请重新输入地址','msg_en':'Can not calculate the distance! Please enter address again!'}
			return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
		distance_row = response_dict["rows"][0]["elements"][0]
		if distance_row["status"] != "OK":
			response = {'code':-4,'msg':'收货地址无法计算距离，请重新输入地址','msg_en':'Can not calculate the distance! Please enter address again!'}
			return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
		distance = "%.1f" % (distance_row["distance"]["value"] / 1000000.0)
	except:
		response = {'code':-4,'msg':'收货地址无法计算距离，请重新输入地址','msg_en':'Can not calculate the distance! Please enter address again!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	
	# print response_dict
	response = {'code':0,'msg':'success',"distance":distance}
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	
	
# 计算运费
def calculate_freight(request):
	response = {}
	total_price = None
	distance = None
	code = None
	if 'total_price' in request.GET:
		total_price = request.GET['total_price']
	else:
		code = -100		
	if 'distance' in request.GET:
		distance = request.GET['distance']
	else:
		code = -100				
	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		
	global_set = GlobalSetting.objects.all()[0]
	# 运费
	print "distance= ",distance
	freight_price = 0
	if float(total_price) < global_set.freight_thres:
		freight_price = float("%.1f" % (float(distance) / (float)(1.6)))
	response = {'code':0,'msg':'success','freight_price':freight_price}	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 计算税
def calculate_tax(request):
	response = {}
	total_price = None	
	code = None
	if 'total_price' in request.GET:
		total_price = request.GET['total_price']
	else:
		code = -100		
	if code == -100:
		response = {'code':-100,'msg':'请求参数不完整，或格式不正确！','msg_en':'Request parameter incomplete or incorrectly formatted!'}
		return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		
	global_set = GlobalSetting.objects.all()[0]			
	# 税
	tax = float("%.1f" %(float(total_price) * float(global_set.tax_rate)))	
	response = {'code':0,'msg':'success','tax':tax}	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 全局设置
def get_global_conf(request):
	response = {}
	global_set = GlobalSetting.objects.all()[0]
	response = {'code':0,'msg':'success'}
	response['working_hours'] = global_set.working_hours
	response['customer_service'] = global_set.customer_service
	response['policy_link'] = global_set.policy_link
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

def delete_token(request):
	response = {}
	print request.session
	request.session = {}
	# for key in request.session:
	# 	del request.session[key]
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

########################### 
#
#	Other Module Interface
#
########################### 

# 获取banner list
def get_banner_list(request):
	response = {}
	response = {'code':0,'msg':'success'}
	banner_list = []
	all_banner_objs = BannerImg.objects.order_by('-priority')
	for banner_obj in all_banner_objs:
		temp_banner = {}
		temp_banner['img'] = "http://resource.jindouyunonline.com:8001/media/" + banner_obj.img.name
		temp_banner['priority'] = banner_obj.priority
		temp_banner['link'] = banner_obj.link
		banner_list.append(temp_banner)
	response['banner_list'] = banner_list
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