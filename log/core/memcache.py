#!/usr/bin/python

import cPickle as pickle
import mmap
import os
import settings

MEMSIZE = 1024 * 128
BankAddr = settings.PROJECT_HOME + '/core/%s'

def save_mem(obj, custom='log'):
	bankname = BankAddr%custom
	mem = pickle.dumps(obj)
	lenth = len(mem)
	fd = open(bankname, 'w+')
	fd.write(mem)
	fd.write('\0' * (MEMSIZE - lenth))
	fd.close()
	os.chmod(bankname, 0777)

def refresh_mem(obj, custom='log'):
	bankname = BankAddr%custom
	mem = pickle.dumps(obj)
	lenth = len(mem)
	fd = open(bankname, 'a+')
	mshare = mmap.mmap(fd.fileno(), MEMSIZE)
	mshare[:] = '%s%s'%(mem, '\0' * (MEMSIZE - lenth))
	mshare.flush()
	mshare.close()
	fd.close()

def get_mem(custom='log'):
	bankname = BankAddr%custom
	fd = open(bankname, 'r+')
	mshare = mmap.mmap(fd.fileno(), MEMSIZE)
	fd.close()
	mobj = pickle.loads(mshare[:])
	mshare.close()
	return mobj

def save(obj, custom):
	bankname = BankAddr%custom
	mem = pickle.dumps(obj)
	fd = open(bankname, 'w+')
	fd.write(mem)
	fd.close()
	os.chmod(bankname, 0777)
	
def get(obj, custom):
	bankname = BankAddr%custom
	fd = open(bankname, 'a+')
	buff = fd.read()
	fd.close()
	return pickle.loads(buff)
