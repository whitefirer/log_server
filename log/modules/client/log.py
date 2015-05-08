#!usr/bin/python
# -*- coding: UTF-8 -*-

from core import dbsqlite3
from core.err_code import *
from core.log import DEBUG
import json, time, hashlib, re
import pdb

def log_add(db, args):
	DEBUG("ars" + str(args))
	retobj = {}
	log = {}

	argObj = args['argObj']
	if argObj is None:
		retobj['RetCode'] = NOT_ENOUGH_PARAS
		return retobj
		
	appname = argObj['appName']
	soft_version = argObj['softVersion']
	caused_by =  'Unknow'
	os_version = argObj['osVersion']
	machine = argObj['machine']
	up_time =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	other_message = argObj['otherMessage']
	logcontent = argObj['logcontent']
	#log_md5 = argObj['md5'] ,
	#frequency = argObj['frequency'],
		
	if logcontent is not None:
		log_md5 = hashlib.md5(logcontent).hexdigest()
		pattern = re.compile(r'caused by:(?P<sign>.*)\n')
		caused_by = pattern.findall(logcontent)[0]
		cond = "WHERE appname='%s' and soft_version='%s' and md5='%s'" %(appname, soft_version,log_md5)
		db.select('tb_log', cond=cond)
		for dur in db.cur:
			dbobj = dbsqlite3.row_to_dict("tb_log", dur)
			if (machine == dbobj['machine'])\
				and (os_version == dbobj['os_version']):
				
				log['up_time'] = up_time
				log['frequency'] = dbobj['frequency'] + 1
	
				cond = "WHERE id=%d" %(dbobj['id'])
				db.update("tb_log", log, cond=cond)
				retobj['RetCode'] = CMD_SUCCESS
				retobj['RetObj'] = None
				return retobj
			else:
				continue
		log = {
			'appname' : appname,
			'soft_version' : soft_version,
			'caused_by' : caused_by,
			'os_version' : os_version,
			'machine' : machine,
			'up_time' : up_time,
			'other_message' : other_message,
			'logcontent' : logcontent,
			'md5' : log_md5,
			'frequency' : 1,
		}
		db.insert("tb_log", log)

	retobj['RetCode'] = CMD_SUCCESS
	retobj['RetObj'] = None

	return retobj
	