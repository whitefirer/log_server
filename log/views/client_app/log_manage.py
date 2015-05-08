from core.log import DEBUG
from core.commonUtils import *
from core.err_code import *

def log_add(request, args):
	DEBUG("running in " + args['func'] + str(args)) 
	ret = callService("client.log.log_add", request, args)
	if ret['RetCode'] == CMD_SUCCESS:
		resObj = buildSuccessData(ret['RetObj'])
	else:
		resObj = buildFailerData(ret['RetCode'])
	return resObj
