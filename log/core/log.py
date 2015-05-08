#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging, traceback
from logging.handlers import RotatingFileHandler
from commands import getoutput
from conf import config
import os
import platform

def file_check(logfile):
	if not os.path.exists(logfile):
		cmd = 'touch %s'%logfile
		getoutput(cmd)
		cmd = 'chmod 777 %s'%logfile
		getoutput(cmd)

def loginit(trace):
	trace_len = len(trace)
	trace = trace[trace_len - 2][:2]
	sysstr = platform.system()
	if (sysstr == "Windows"):
		callname = ((trace[0].split('\\'))[-1])
	else:
		callname = ((trace[0].split('/'))[-1])
		
	logfilehead = (callname.split('.')[0]).split('_')[0]

	file_name = config.LOG_FILE_PATH + logfilehead + '.log'
	file_check(file_name)
	lineid = trace[1]
	logger = logging.getLogger()

	handle = RotatingFileHandler(file_name,'a',config.LOG_MAX_LEN,2)
	formatter = logging.Formatter('%(process)d [%(asctime)s %(callname)s %(lineid)d] %(levelname)s: %(message)s')
	handle.setFormatter(formatter)
	logger.addHandler(handle)
	logger.setLevel(logging.NOTSET)

	return logger,handle,{'lineid':lineid, 'callname':callname}

def DEBUG(msg, *args):
	if config.LOG_LEVEL < 5:return
	logger, handle, extra = loginit(traceback.extract_stack())
	kwargs = {'extra':extra, 'exc_info':1}
	logger.debug(msg, *args, **kwargs)
	_close(handle, logger)
def INFO(msg, *args):
	if config.LOG_LEVEL < 4:return

	logger, handle, extra = loginit(traceback.extract_stack())
	kwargs = {'extra':extra, 'exc_info':1}
	logger.info(msg, *args, **kwargs)
	_close(handle, logger)

def WARNING(msg, *args):
	if config.LOG_LEVEL < 3:return
	logger, handle, extra = loginit(traceback.extract_stack())
	kwargs = {'extra':extra, 'exc_info':1}
	logger.warning(msg, *args, **kwargs)
	_close(handle, logger)

def ERROR(msg, *args):
	if config.LOG_LEVEL < 2:return
	logger, handle, extra = loginit(traceback.extract_stack())
	kwargs = {'extra':extra, 'exc_info':1}
	logger.error(msg, *args, **kwargs)
	_close(handle, logger)

def CRITICAL(msg, *args):
	if config.LOG_LEVEL < 1:return
	logger, handle, extra = loginit(traceback.extract_stack())
	kwargs = {'extra':extra, 'exc_info':1}
	logger.critical(msg, *args, **kwargs)
	_close(handle, logger)

def _close(handle,logger):
	try:
		handle.flush()
		logger.removeHandler(handle)
		logging.shutdown()
	except Exception:
		pass
