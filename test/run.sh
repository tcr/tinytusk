#!/bin/bash

# Error on error
set -e

# Create temp directory
TMPDIR=`mktemp -d 2>/dev/null || mktemp -d -t 'tinytusk'`
# echo $TMPDIR

# Add files
echo $'#include <stdio.h>\n\nint main () {\n\tprintf(\"test was a success\\n\");\n\treturn 0;\n}\n' > $TMPDIR/main.c
tar -cjf test.tar.gz -C $TMPDIR .

# Test with docker
cat test.tar.gz | docker run -a stdin -a stdout -a stderr -i tinytusk /bin/bash -c "/tusk/run.sh --run"
