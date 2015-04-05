#!/bin/bash

# Stop on error
set -e

# Load input into /tusk/source
mkdir source
tee | tar -jxf - -C source 

# Compile, output to stderr
gcc -Wall -o output source/*.c 1>&2

# Cat resulting binary to stdout
if [[ $1 == --run ]]; then
    ./output
else
	cat ./output
fi
