# -*- coding:utf-8 -*-
import hashlib
import web
import xml.etree.ElementTree as etree
import time
import os
import urllib2
import json

class WeixinInterface:
	def __init__(self):
		self.app_root = os.path.dirname(__file__)
		self.templates_root = os.path.join(self.app_root, "templates")
		self.render = web.template.render(self.templates_root)
	
	def GET(self):
		# 获取输入参数
		data = web.input()
		signature = data.signature
		timestamp = data.timestamp
		nonce = data.nonce
		echostr = data.echostr
		# 自己的token
		token = "everlose"
		#字典序排序
		t_list = [token, timestamp, nonce]
		t_list.sort()
		sha1 = hashlib.sha1()
		map(sha1.update, t_list)
		hashcode = sha1.hexdigest()

		#如果是来自微信的请求,则回复echostr
		if hashcode == signature:
			return echostr
	
	def POST(self):
		str_xml = web.data() #获取post的数据
		tree = etree.parse(str_xml)   #进行xml解析
		root = tree.getroot()
		content = root[4].text #获取用户输入的内容
		msgType = root[3].text
		fromUser = root[1].text
		toUser = root[0].text
		reply_content = u"%s,我知道是你,你刚才说'%s',我也对你说'%s',哈哈哈,更多功能,敬请期待" % (fromUser, content, content)
		return self.render.reply_text(fromUser, toUser, int(time.time()), reply_content)
