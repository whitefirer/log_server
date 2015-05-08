#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import struct
import cPickle as pickle
import time
import settings
from core import dbsqlite3
from core.err_code import *

from log import ERROR, INFO,DEBUG

def service_get_msg(RetCode):
	retstruct = {'RetObj': None}
	retstruct['RetCode'] = RetCode
	return retstruct

def ws_call(*args):
	arg = args[-1]
	req = args[-2]
	ws_name = args[-3]

	obj_ret = service_handle(ws_name, arg)
	return obj_ret

def service_handle(s_name, arg):
	calllist = s_name.split('.')
	modulepath = calllist[:-1]
	funname = calllist[-1]

	db = dbsqlite3.sqlitedb()

	DEBUG("Function name %s" % funname)

	try:
		service = __import__('modules'+'.'+'.'.join(modulepath), fromlist=['from modules import',])
	except ImportError:
		ERROR('Import module failed. [%s]'%s_name)
		return service_get_msg(FRAME_ERR)

	if hasattr(service, funname):
		funobj = getattr(service, funname)
	else:
		ERROR('There is no %s in %s'%(funname, modulepath))
		return service_get_msg(FRAME_ERR)

	del service

	try:
		funret = funobj(db, arg)
	except Exception,arg:
		ERROR('Error in %s: [%s]'%(s_name, arg))
		return service_get_msg(FRAME_ERR)

	finally:
		del funobj, db

	RetCode = funret.get('RetCode')
	retstruct = service_get_msg(RetCode)
	retstruct['RetObj'] = funret.get('RetObj', None)

	return retstruct
