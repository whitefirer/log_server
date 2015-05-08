import os
import sys
import zipfile
import tempfile
import filemanage
import settings
from log import DEBUG,ERROR

def usage():
	print sys.argv[0] + ' source target rc'
	sys.exit(0)

def _installrc(fapk, rc):
	t = 'res' + os.path.sep + 'raw' + os.path.sep + 'rc.txt'
	fapk.writestr(t, rc)

def _package(fapk, src, parent=os.path.sep):

	for t in os.listdir(src):
		curr = os.path.join(parent, t)
		fpath = os.path.join(src, t)

		if os.path.isfile(fpath):
			fapk.write(fpath, os.path.join(parent, t))
		else:
			_package(fapk, fpath, curr)  

def _sign_public(src, tar):
	cmd = 'java -jar '
	cmd += settings.PROJECT_HOME + 'lib' + os.path.sep + 'signapk.jar '
	cmd += settings.PROJECT_HOME + 'public' + os.path.sep + 'platform.x509.pem '
	cmd += settings.PROJECT_HOME + 'public' + os.path.sep + 'platform.pk8 ' + src + ' ' + tar

	DEBUG(cmd)

	ret = os.popen(cmd)
	if ret != 0:
		ERROR("exec cmd %s error" % cmd)
		return False
	
	return True

def check(tar):
	ret = False	
	print 'checking ' + tar

	f = zipfile.ZipFile(tar, 'r')
	for n in f.namelist():
		if n.endswith('rc.txt'): ret = True

	f.close()
	return ret

def Sign(src, tar, rc):
	op = filemanage.Deleter(False)

	unzip_dir = os.path.join(settings.PROJECT_HOME + 'dummy')
	op.DeleteFolder(unzip_dir)
	
	f = zipfile.ZipFile(src, 'r')
	f.extractall(unzip_dir)
	f.close()

	meta = os.path.join(unzip_dir, 'META-INF')
	op.DeleteFolder(meta)

	frc = os.path.join(unzip_dir, 'res' + os.path.sep + 'raw' + os.path.sep + 'rc.txt')
	op.DeleteFile(frc)

	tmp = tempfile.mkstemp(prefix='ny')
	f = zipfile.ZipFile(tmp[1], 'w', zipfile.ZIP_DEFLATED)

	_package(f, unzip_dir)

	DEBUG("temp0 is %s" % tmp[0])
	DEBUG("temp1 is %s" % tmp[1])

	DEBUG("rc is %s" % rc)

	_installrc(f, rc)

	f.close()

	_sign_public(tmp[1], tar)
	
if '__main__' == __name__:

	if len(sys.argv) < 4:
		usage()
	
	Sign(sys.argv[1], sys.argv[2], sys.argv[3])
