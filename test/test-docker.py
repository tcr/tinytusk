import subprocess
import os
import cStringIO
import StringIO
import tarfile
import gzip
import time

# Relative imports hack
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from builder import build_test

# Build a tar file.

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

result, buildinfo = build_test(c.getvalue())

if buildinfo:
	print buildinfo,

if result != 'success!\n' or buildinfo != '':
	raise Exception('test failed')
else:
	print 'test successful'
