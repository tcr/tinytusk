from flask import Flask, make_response, request
from flask import render_template
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
from builder import build_test, build_binary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Build endpoint. Accepts a .tar.gz,
# returns a binary and its compilation messages
@app.route('/api/build', methods = ['POST'])
def api_build():
	result, info = build_binary(request.get_data())

	datagen, headers = multipart_encode([
		MultipartParam(name="result", value=result),
		MultipartParam(name="info", value=info)
	], boundary='lol')
	response = make_response('\r\n'.join(list(datagen))[:-4])
	response.headers = headers
	return response

# Test endpoint. Accepts a .tar.gz,
# returns a test result and its compilation messages
@app.route('/api/test', methods = ['POST'])
def api_test():
	result, info = build_test(request.get_data())

	datagen, headers = multipart_encode([
		MultipartParam(name="result", value=result),
		MultipartParam(name="info", value=info)
	], boundary='lol')
	response = make_response('\r\n'.join(list(datagen))[:-4])
	response.headers = headers
	return response

if __name__ == "__main__":
    app.run(debug=True)
