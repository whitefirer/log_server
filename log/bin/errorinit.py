import io
import sys
import os

INFILE_DEFAULT="./core/errorcode.def"
OUTFILE_DEFAULT="./core/err_code.py"

def print_head(f_out):
	f_out.write("#!/usr/bin/python\n# -*- coding: UTF-8 -*-\n\n")
	return

def print_tail(f_out):
	data = '''
def print_retmsg(buff):
	print '\\n%% \%s\\n' % buff'''

	f_out.write(data)
	return

def print_error_code(f_in, f_out):
	for line in f_in.readlines():
		m = line.split(', ')
		f_out.write(m[0] + " = " + m[1] + "\n")
	f_out.write("\n")
	return

def print_error_msg_ch(f_in, f_out):
	f_in.seek(0)
	f_out.write("err_desc_ch = {\n")

	for line in f_in.readlines():
		m = line.split(', ')
		f_out.write("\t" + m[0] + ":" + m[3].replace("\n", "") + ",\n")

	f_out.write("}\n\n")

	return

def print_error_msg_en(f_in, f_out):
	f_in.seek(0)
	f_out.write("err_desc_en = {\n")

	for line in f_in.readlines():
		m = line.split(', ')
		f_out.write("\t" + m[0] + ":" + m[2] + ",\n")

	f_out.write("}\n")

	return

if __name__ == '__main__':
	argc = len(sys.argv)
	if argc != 3:
		infile = INFILE_DEFAULT
		outfile = OUTFILE_DEFAULT
	else:
		infile = sys.argv[1]
		outfile = sys.argv[2]

	#clear original file
	os.remove(outfile)
	
	f_in = open(infile,'r')
	f_out = open(outfile, 'a')

	print_head(f_out)

	print_error_code(f_in, f_out)

	print_error_msg_ch(f_in, f_out)

	print_error_msg_en(f_in, f_out)

	print_tail(f_out)

	f_in.close()
	f_out.close()
