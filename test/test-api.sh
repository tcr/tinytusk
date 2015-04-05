#!/bin/sh

cd $(dirname $0)

python output.py > /tmp/output.tar.gz
http POST http://127.0.0.1:5000/api/test < /tmp/output.tar.gz
