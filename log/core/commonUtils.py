from django.utils import simplejson
import os
import re
import datetime
import time
from core import dispatch

def buildSuccessData(data):
	return _buildData(0, data=data)

def buildFailerData(errorCode = 0, errorMsg=None):
	return _buildData(errorCode, errorMsg)

def _buildData(errorCode=None, errorMsg=None, data=None):
	resObj = {}
	retObj = {
		"errorCode":errorCode, 
		"errorMsg":errorMsg,
	}
	resObj["retObj"] = retObj
	resObj["data"] = data

	return resObj

def callService(wsName, request, arg):
	return dispatch.ws_call(wsName, request, arg)
