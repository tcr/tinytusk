import subprocess
import os
import cStringIO
import StringIO
import tarfile
import gzip
import time

c = cStringIO.StringIO()
t = tarfile.open(mode='w:gz', fileobj=c)

string = StringIO.StringIO()
string.write("""
#include <stdio.h>

int main () {
	printf("success!\\n");
	return 0;
}
""")
string.seek(0)
info = tarfile.TarInfo(name="main.c")
info.size=len(string.buf)
info.mtime=time.time()
t.addfile(tarinfo=info, fileobj=string)
t.close()

cwd = os.path.dirname(os.path.realpath(__file__))

p = subprocess.Popen(['docker', 'run', '-a', 'stdin', '-a', 'stdout', '-a', 'stderr', '-i', 'tinytusk', '/bin/bash', '-c', '/tusk/run.sh --run'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
stdout, stderr = p.communicate(input=c.getvalue())

print stderr,

if stdout != 'success!\n' or stderr != '':
	raise Exception('test failed')
else:
	print 'test successful'
