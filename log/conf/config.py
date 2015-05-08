#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.append("../");
import settings
import os.path as op

DEBUG = True

DBPATH_POOL = {
	'log':settings.PROJECT_HOME + '/db/log.db',
	'wsession':settings.PROJECT_HOME + '/db/log.db'
}

LOG_FILE_PATH = settings.PROJECT_HOME + '/logs/'

LOG_LEVEL = 5
LOG_MAX_LEN = 102400
