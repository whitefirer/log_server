import os
import re
import json
import datetime
import time
import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.utils.safestring import mark_safe, SafeData
import django.utils.translation.trans_real
from func_maps import *
from django.http import SimpleCookie, HttpRequest
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from core.err_code import *
from core.log import DEBUG
import pdb

# test this please access "http://200.1.1.92:8080/cliapi/?fc=login"
def cliapiDispatch(fc, request, args):
	func = func_dic_cliapi[fc]
	if func is None:
		return None
	return func(request, args)

# test this please access "http://200.1.1.92:8080/api/?fc=login"
def apiDispatch(fc, request, args):
	func = func_dic_api[fc]
	if func is None:
		return None
	return func(request, args)

@csrf_exempt
def cliapi_action(request):
	args = {}
	func = request.REQUEST.get("fc")
	argObj = request.REQUEST.get("argObj")
	if argObj is None:
		args["argObj"] = argObj
	else:
		exec('args["argObj"]='+request.REQUEST.get("argObj"))
	args["func"] = func
	ret = cliapiDispatch(func, request, args)
	resObj = json.JSONEncoder().encode(ret)
 
	DEBUG("obj " + str(resObj))

	return HttpResponse(resObj)

@csrf_exempt
def api_action(request):
	args = {}
	func = request.REQUEST.get("fc")
	argObj = request.REQUEST.get("argObj")
	DEBUG("fc" + func)
	DEBUG("argobj" + str(argObj))
	if argObj is None:
		args["argObj"] = argObj
	else:
		exec('args["argObj"]='+request.REQUEST.get("argObj"))
	args["func"] = func
	DEBUG("argobj" + str(args))
	ret = apiDispatch(func, request, args)

	resObj = json.JSONEncoder().encode(ret)

	DEBUG("obj " + str(resObj))

	return HttpResponse(resObj)

def valid_session(request, arg):
	state = False
	return True
	if request.session.get_expiry_date() >= datetime.datetime.now():
		if request.session.get(arg, None):
			state = True
		else:
			state = False
	else:
		state = False
	return state

def invoke_template(request, template_name):
	validOK = valid_session(request, "userInfo")
	if validOK is not True:
		template_name = 'index.html'
		
	return render_to_response(template_name)

def static_pages(request, template_name):
	if template_name == '':
		template_name = 'index.html'
	return invoke_template(request, 'pages/' + template_name)

class Log(object):
	@staticmethod
	def list(request):
		return render_to_response('log/loglist.htm')

	#@staticmethod
	#def add(request):
	#	return HttpResponseRedirect('')

