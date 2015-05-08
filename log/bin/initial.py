#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import db_init
import cPickle as pickle
import mmap

sys.path.append(".");

MEMSIZE = 1024 * 128
BankAddr = './core/%s'

def save_mem(obj, custom='log'):
	bankname = BankAddr%custom
	mem = pickle.dumps(obj)
	lenth = len(mem)
	fd = open(bankname, 'w+')
	fd.write(mem)
	fd.write('\0' * (MEMSIZE - lenth))
	fd.close()
	os.chmod(bankname, 0777)

DB_DIR = 'db/'
DBXMLPATH_POOL = { 
	'log': DB_DIR + 'log.xml',
}

DBSQLPATH_POOL = {
	'log': DB_DIR + 'log.default',
}

DBPATH_POOL = {
	'log': DB_DIR + 'log.db',
}

def checkpath(filepath):
	if os.access(filepath, os.F_OK):
		try:
			os.remove(filepath)
		except OSError:
			pass
	fd = open(filepath, 'w+')
	fd.close()
	for filename in os.listdir(DB_DIR):
		os.chmod('%s/%s'%(DB_DIR, filename), 0777)

def init_db():
	map(checkpath, DBPATH_POOL.values())
	if not db_init.db_createtable(DBPATH_POOL, DBXMLPATH_POOL):
		print DBPATH_POOL.values()
		print DBPATH_POOL
		print DBXMLPATH_POOL
		print('Autoinit dbinit failed.')
		return False

	if not db_init.db_initdata(DBPATH_POOL, DBSQLPATH_POOL):
		print('Autoinit datainit failed.')
		return False

	tablelist = db_init.db_initcols(DBXMLPATH_POOL)
	mem = {'tablelist': tablelist}
	save_mem(mem, custom='log')

	return True

if __name__ == '__main__':
	init_db()
