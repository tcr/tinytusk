import subprocess

# build and run script
def build_test(input):
	p = subprocess.Popen(['docker', 'run', '-a', 'stdin', '-a', 'stdout', '-a', 'stderr', '-i', 'tinytusk', '/bin/bash', '-c', '/tusk/run.sh --run'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	result, buildinfo = p.communicate(input=input)
	return (result, buildinfo)

# build script, result in program
def build_binary():
	p = subprocess.Popen(['docker', 'run', '-a', 'stdin', '-a', 'stdout', '-a', 'stderr', '-i', 'tinytusk', '/bin/bash', '-c', '/tusk/run.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	result, buildinfo = p.communicate(input=input)
	return (result, buildinfo)
