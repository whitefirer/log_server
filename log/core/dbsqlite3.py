#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3 as sqlite
from conf import config
from core import memcache
import pdb

membody = memcache.get_mem()
tablelist = membody.get('tablelist', {})
SQL_ERROR = -1
SQL_SUCCESS = 0

def row_to_dict(tabname, row, dbname='log'):
	obj={}
	map(obj.__setitem__, tablelist[dbname][tabname], row)
	return obj

class sqlitedb:
	def __init__(self):
		self.connlist = {}
		conn = sqlite.connect(config.DBPATH_POOL.get('log'))
		self.connlist['log'] = conn

	def __del__(self):
		for conn in self.connlist.values():
			conn.close()

	def connect(self, dbname):
		conn = self.connlist.get(dbname, None)
		if conn == None:
			conn = sqlite.connect(config.DBPATH_POOL.get(dbname))
			self.connlist[dbname] = conn
		return conn

	def select(self, table, cond='', field='*', offset=-1, limit=-1, dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		sql = 'select %s from %s %s limit %d offset %d'%(field, table , cond, limit , offset)
		try:
			self.cur.execute(sql)
		except sqlite.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS

	def rowcount(self, table, cond='', dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		sql = 'select count(*) from %s %s'%(table, cond)
		try:
			self.cur.execute(sql)
		except sqlite.OperationalError:
			return SQL_ERROR
		count = self.cur.fetchall()[0][0]
		return count

	def insert(self, table, obj, dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		columns = tablelist[dbname][table]
		columnlist = [k for k in obj.keys() if k in columns and k.lower() !='id']
				
		sql = 'insert into %s (%s) values(%s)'%(table,','.join(columnlist), 
								','.join([':%s'%k for k in columnlist]))
		try:
			self.cur.execute(sql,obj)
		except sqlite.OperationalError:
			conn.rollback()
			return SQL_ERROR
		
		rowid = self.cur.lastrowid
		if rowid == None:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return rowid

	def delete(self, table, obj=None, cond='', dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		if obj != None:
			if obj.has_key('id'):
				cond = 'where id=:id'
			else:
				cond = 'where %s'%' and '.join(['%s=:%s'%(k,k) for k in obj.keys()])
		
		sql = 'delete from %s %s'%(table, cond)
		if obj == None:obj={}
		try:
			self.cur.execute(sql, obj)
		except sqlite.OperationalError:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return SQL_SUCCESS
	
	def update(self, table, obj=None, cond='', field='', dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		
		if obj != None:		
			columns = tablelist[dbname][table]
			columnlist = [k for k in obj.keys() if k in columns]
			field = 'set %s'%','.join(['%s=:%s'%(k,k) for k in columnlist])
		if cond == '':
			if obj.has_key('id'):
				cond = 'where id=:id'
		
		sql = 'update %s %s %s'%(table, field, cond)
		if obj == None:obj = {}
		try:
			self.cur.execute(sql, obj)
		except sqlite.OperationalError:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return SQL_SUCCESS
	
	def execute(self, table, sql, dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		try:
			self.cur.execute(sql)
		except sqlite.OperationalError:
			conn.rollback()
			return SQL_ERROR
		conn.commit()
		return SQL_SUCCESS

	def insert_ex(self, table, obj, dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		columns = tablelist[dbname][table]
		columnlist = [k for k in obj.keys() if k in columns]
				
		sql = 'insert into %s (%s) values(%s)'%(table,','.join(columnlist), 
								','.join([':%s'%k for k in columnlist]))
		try:
			self.cur.execute(sql,obj)
		except sqlite.OperationalError:
			return SQL_ERROR
		
		rowid = self.cur.lastrowid
		if rowid == None:
			return SQL_ERROR
		return rowid
	
	def delete_ex(self, table, obj=None, cond='', dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		if obj != None:
			if obj.has_key('id'):
				cond = 'where id=:id'
			else:
				cond = 'where %s'%' and '.join(['%s=:%s'%(k,k) for k in obj.keys()])
		
		sql = 'delete from %s %s'%(table, cond)
		if obj == None:obj={}
		try:
			self.cur.execute(sql, obj)
		except sqlite.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS
	
	def update_ex(self, table, obj=None, cond='', field='', dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
				
		if obj != None:
			columns = tablelist[dbname][table]
			columnlist = [k for k in obj.keys() if k in columns]
			field = 'set %s'%','.join(['%s=:%s'%(k,k) for k in columnlist])
		if cond == '':
			if obj.has_key('id'):
				cond = 'where id=:id'
		
		sql = 'update %s %s %s'%(table, field, cond)
		if obj == None:obj={}
		try:
			self.cur.execute(sql, obj)
		except sqlite.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS

	def execute_ex(self, table, sql, dbname='log'):
		conn = self.connect(dbname)
		self.cur = conn.cursor()
		try:
			self.cur.execute(sql)
		except sqlite.OperationalError:
			return SQL_ERROR
		return SQL_SUCCESS

	def create_function(self, name, num_params, func, dbname='log'):
		conn = self.connect(dbname)
		conn.create_function(name, num_params, func)

	def rollback(self, dbname='log'):
		self.connlist.get(dbname).rollback()
	
	def commit(self, dbname='log'):
		self.connlist.get(dbname).commit()
