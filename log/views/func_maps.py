#!usr/bin/python
# -*- coding: UTF-8 -*-

from django.conf import settings
import traceback

from views.client_app.log_manage import *
from views.log.log_manage import *


func_dic_cliapi = {
	'log_add':log_add,
}

func_dic_api = {
	'log_list': log_list,
}
