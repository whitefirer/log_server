#!/usr/bin/env python

import httplib, urllib
from django.template import Template, Context  
from django.conf import settings  
settings.configure() 
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def simple_post(function):
	
	args1 = {
		'fc': 'log_list',
		'cookie':'3l34l23l23dl2l3k4l423l42l43k4354l45l543',
		'argObj':{
			"page":1,
			"pagelog":5,
		}
	}
	
	args2 = {
		'fc': 'log_add',
		'cookie':'3l34l23l23dl2l3k4l423l42l43k4354l45l543',
		'argObj':{
			'appName' : 'testAPP2',
			'softVersion' : '1.1',
			'osVersion' : 'Android2.3',
			'machine' : 'MX',
			'otherMessage' : 'sodeishine',
			'logcontent' : 'there\r\nhere',
		}
	}
	newarg = args2

	params = urllib.urlencode(newarg)
	headers = {'Accept': 'text/html', 'User-Agent': 'Mozilla',
		'Content-Type': 'application/x-www-form-urlencoded'}
	server = '192.168.1.51:8080'
	#path = '/api?fc=' + newarg['fc']
	path = '/cliapi?fc=' + newarg['fc']

	conn = httplib.HTTPConnection(server)
	conn.request("POST", path, params, headers)
	
	r1 = conn.getresponse()
	print r1.status, r1.reason
	data1 = r1.read()
	print data1
	conn.close()

if __name__ == '__main__':
	simple_post("ff")
