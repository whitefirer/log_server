#!usr/bin/python
# -*- coding: UTF-8 -*-

from core import dbsqlite3
from core.err_code import *
from core.log import DEBUG,ERROR
import time, json, re, hashlib
import pdb

def log_list(db, args):
	list=[]
	retobj = {}

	DEBUG("args " + str(args))
	argObj = args['argObj']
	if argObj is None:
		retobj['RetCode'] = NOT_ENOUGH_PARAS
		return retobj
	
	total = 0
	page = 1
	pagetotal = 1
	pagelog = 5
	
	page = argObj['page']
	pagelog = argObj['pagelog']
	order_by = argObj['order_by']
	filter = argObj['filter']
	filter_data = argObj['filter_data']
	if order_by is None:
		cond = None
	else:
		cond = 'order by %s' %(order_by)
	if filter is None :
		cond = 'order by %s' %(order_by)
	elif filter == 'all':
		cond = 'order by %s' %(order_by)
	else:
		cond = 'WHERE %s is \'%s\' order by %s' %(filter,filter_data, order_by)
	
	ret = db.select('tb_log', cond=cond, field='count(*)')
	try:
		total = db.cur.fetchall()[0][0]
	except IndexError:
		pass
		
	pagetotal = (total + pagelog - 1) // pagelog
	offset = total-page*pagelog
	
	if offset > 0 :
		ret = db.select('tb_log', cond=cond, offset=offset, limit=pagelog)
	else:
		ret = db.select('tb_log', cond=cond, offset=0, limit=pagelog+offset)
	for dur in db.cur:
		dbobj = dbsqlite3.row_to_dict("tb_log", dur)
		log = {
			'id' : dbobj['id'],
			'caused_by' : dbobj['caused_by'],
			'appname' : dbobj['appname'],
			'soft_version' : dbobj['soft_version'],
			'os_version' : dbobj['os_version'],
			'machine' : dbobj['machine'],
			'up_time' : dbobj['up_time'],
			'other_message' : dbobj['other_message'],
			'md5' : dbobj['md5'],
			'logcontent' : dbobj['logcontent'],
			'frequency' : dbobj['frequency'],
		}
		list.append(log)
			
	lists = {
		'pagetotal' : pagetotal,
		'total' : total,
		'list' : list
	}
	retobj['RetObj'] = lists;
	retobj['RetCode'] = CMD_SUCCESS

	return retobj
