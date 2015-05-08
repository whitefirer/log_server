#!/usr/bin/python
# -*- coding: UTF-8 -*-

CMD_SUCCESS = 0
NOT_ENOUGH_PARAS = 1
TOO_MANY_PARAS = 2
UNACCP_PARAS = 3
XML_ERR = 4
EXEC_CMD_ERR = 5
SYSTEM_ERR = 6
SYSCALL_ERR = 7
DB_ERR = 8
OPEN_DB_ERR = 9
USER_NOT_EXIST = 10
FRAME_ERR = 11
USER_ALREADY_EXIST = 11
USER_PASSWD_ERR = 12
GROUP_NOT_EXIST = 13
GROUP_ALREADY_EXIST = 14
SEGMENT_NOT_EXIST = 15
SEGMENT_ALREADY_EXIST = 16
CONFIG_NOT_EXIST = 17
CONFIG_ALREADY_EXIST = 18
INVALID_CONFIG_FILE = 19

err_desc_ch = {
	CMD_SUCCESS:"执行成功",
	NOT_ENOUGH_PARAS:"参数不够",
	TOO_MANY_PARAS:"参数太多",
	UNACCP_PARAS:"参数错误",
	XML_ERR:"XML解析错误",
	EXEC_CMD_ERR:"执行命令错误",
	SYSTEM_ERR:"系统错误",
	SYSCALL_ERR:"系统调用错误",
	DB_ERR:"数据库错误",
	OPEN_DB_ERR:"打开数据库失败",
	USER_NOT_EXIST:"用户不存在",
	FRAME_ERR:"Frame错误",
	USER_ALREADY_EXIST:"用户已经存在",
	USER_PASSWD_ERR:"用户名或密码错误",
	GROUP_NOT_EXIST:"组不存在",
	GROUP_ALREADY_EXIST:"组已经存在",
	SEGMENT_NOT_EXIST:"字段不存在",
	SEGMENT_ALREADY_EXIST:"字段已经存在",
	CONFIG_NOT_EXIST:"配置文件不存在",
	CONFIG_ALREADY_EXIST:"配置文件已经存在",
	INVALID_CONFIG_FILE:"配置文件不合法",
}

err_desc_en = {
	CMD_SUCCESS:"Command success",
	NOT_ENOUGH_PARAS:"Not enough parameters",
	TOO_MANY_PARAS:"Too many parameters",
	UNACCP_PARAS:"Invalid parameters",
	XML_ERR:"XML Error",
	EXEC_CMD_ERR:"Execute Command Error",
	SYSTEM_ERR:"System error",
	SYSCALL_ERR:"System call error",
	DB_ERR:"Database error",
	OPEN_DB_ERR:"Open database error",
	USER_NOT_EXIST:"User not exist",
	FRAME_ERR:"Frame Erro",
	USER_ALREADY_EXIST:"User already exist",
	USER_PASSWD_ERR:"Password and username donot match",
	GROUP_NOT_EXIST:"Group not exist",
	GROUP_ALREADY_EXIST:"Group already exist",
	SEGMENT_NOT_EXIST:"Segment not exist",
	SEGMENT_ALREADY_EXIST:"Segment already exist",
	CONFIG_NOT_EXIST:"Config file not exist",
	CONFIG_ALREADY_EXIST:"Config file already exists",
	INVALID_CONFIG_FILE:"Invalid config file",
}

def print_retmsg(buff):
	print '\n%% \%s\n' % buff