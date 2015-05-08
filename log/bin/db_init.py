#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3
from xml.dom import minidom

def db_connect(dbpath):
	try:
		conn = sqlite3.connect(dbpath)
	except:
		return None

	return conn

def init_cols(xmlpath):
	singlefile = {}
	try:
		xmldoc = minidom.parse(xmlpath)
	except:
		return singlefile

	filelist = xmldoc.getElementsByTagName('file')

	for index in range(len(filelist)):
		table=filelist[index]
		tablename=table.attributes['name'].value
		fieldlist=table.getElementsByTagName('field')
		columnlist=[]

		for i in range(len(fieldlist)):
			name=fieldlist[i].attributes['name'].value
			columnlist.append(name)

		singlefile[tablename]=columnlist

	return singlefile

def db_initcols(xmlpathlist):
	cols = {}
	for dbname, xmlpath in xmlpathlist.items():
		cols[dbname] = init_cols(xmlpath)
	return cols

def createtable(dbpath, xmlpath):
	conn = db_connect(dbpath)
	if conn == None:
		print "connect db %s error" % dbpath
		return False

	cur = conn.cursor()

	try:
		xmldoc = minidom.parse(xmlpath)
	except:
		print "parse xml file %s error" % xmlpath
		return False

	filelist = xmldoc.getElementsByTagName('file')

	for index in range(len(filelist)):
		table=filelist[index]
		tablename=table.attributes['name'].value
		fieldlist=table.getElementsByTagName('field')
		attrlist=[]

		for i in range(len(fieldlist)):
			name=fieldlist[i].attributes['name'].value
			type=fieldlist[i].attributes['type'].value
			caption=fieldlist[i].attributes['caption'].value
			attrlist.append("%s %s %s"%(name,type,caption))

		value=', '.join(attrlist)
		sql = 'create table %s ( %s )'%(tablename, value)
		try:
			cur.execute(sql)
		except:
			pass

	conn.commit()
	conn.close()

	return True

def db_createtable(DBPATH_POOL, xmlpathlist):
	for dbname, dbpath in DBPATH_POOL.items():
		xmlpath = xmlpathlist.get(dbname)
		if xmlpath == None:continue
		if not createtable(dbpath, xmlpath):
			return False
	return True

def datainit(dbpath, sqlpath):
	conn = db_connect(dbpath)
	if conn == None:
		return False
	cur = conn.cursor()
	try:
		sqlfile = file(sqlpath)
	except:
		return False

	sqls = sqlfile.readlines()

	for sql in sqls:
		sql = sql.strip('\n').strip(' ')
		if len(sql) == 0 or sql.startswith('#'):
			continue
		try:
			cur.execute(sql)
		except:
			pass

	conn.commit()
	conn.close()

	return True

def db_initdata(DBPATH_POOL, sqlpathlist):
	for dbname, dbpath in DBPATH_POOL.items():
		sqlpath = sqlpathlist.get(dbname)
		if sqlpath == None:
			continue
		if not datainit(dbpath, sqlpath):
			return False
	return True
