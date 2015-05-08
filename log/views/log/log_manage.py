from core.log import DEBUG
from core.commonUtils import *
from core.err_code import *

def log_list(request, args):
	DEBUG("running in " + args['func'] + str(args)) 
	RetObj = callService("log.log.log_list", request, args)
	
	if RetObj['RetCode'] == CMD_SUCCESS:
		resObj = buildSuccessData(RetObj['RetObj'])
	else:
		resObj = buildFailerData(RetObj['RetCode'])

	return resObj