#!/usr/local/bin/python
#-*-coding:utf-8-*-

#author: jacky
# Time: 15-12-15
# Desc: 短信http接口的python代码调用示例
# https://www.yunpian.com/api/demo.html
# https访问，需要安装  openssl-devel库。apt-get install openssl-devel

import httplib
import urllib
import json
from random import Random
#服务地址
sms_host = "sms.yunpian.com"
voice_host = "voice.yunpian.com"
#端口号
port = 443
#版本号
version = "v2"
#查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
#智能匹配模版短信接口的URI
sms_send_uri = "/" + version + "/sms/single_send.json"
#模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_single_send.json"
#语音短信接口的URI
sms_voice_send_uri = "/" + version + "/voice/send.json"
#语音验证码
voiceCode = 1234
def get_user_info(apikey):
    """
    取账户信息
    """
    conn = httplib.HTTPSConnection(sms_host , port=port)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn.request('POST',user_get_uri,urllib.urlencode( {'apikey' : apikey}))
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def send_sms(apikey, text, mobile):
    """
    通用接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'tpl_id':tpl_id, 'tpl_value': urllib.urlencode(tpl_value), 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def send_voice_sms(apikey, code, mobile):
    """
    通用接口发短信
    """
    params = urllib.urlencode({'apikey': apikey, 'code': code, 'mobile':mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(voice_host, port=port, timeout=30)
    conn.request("POST", sms_voice_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def jindouyun_sms_sender(mobile,code):
    apikey = "eeddfb69fdec492bf95e3c2fb90512b8"
    tpl_id = 1301727
    tpl_value = {'#code#':code}
    response_str =  tpl_send_sms(apikey, tpl_id, tpl_value, mobile)
    print response_str
    return response_str

# 生成随机字符串
def token_str(randomlength=4):
    str = ''
    chars = '0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

if __name__ == '__main__':
    #修改为您的apikey.可在官网（http://www.yuanpian.com)登录后获取
    apikey = "eeddfb69fdec492bf95e3c2fb90512b8"
    #修改为您要发送的手机号码，多个号码用逗号隔开
    # mobile = urllib.quote("+12673933836")
    mobile = "+12673933836"
    #查账户信息
    print(get_user_info(apikey))
    #调用智能匹配模版接口发短信
    #调用模板接口发短信
    tpl_id = 1301727 #对应的模板内容为：您的验证码是#code#【#company#】
    tpl_value = {'#code#':'7284'}
    response_str =  tpl_send_sms(apikey, tpl_id, tpl_value, mobile)
    print response_str.encode('utf-8')