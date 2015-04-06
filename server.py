from flask import Flask, make_response, request
from flask import render_template, send_file
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
from builder import build_test, build_binary
import io
import hashlib
import cStringIO
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Build endpoint. Accepts a .tar.gz,
# returns a binary and its compilation messages
@app.route('/api/build', methods = ['POST'])
def api_build():
	result, info = build_binary(request.get_data())

	datagen, headers = multipart_encode({
		"info": info,
		"result": base64.b64encode(result),
	})
	out = '\r\n'.join(list(datagen))
	return send_file(io.BytesIO(out),
		mimetype=headers['Content-Type'])

# Test endpoint. Accepts a .tar.gz,
# returns a test result and its compilation messages
@app.route('/api/test', methods = ['POST'])
def api_test():
	result, info = build_test(request.get_data())

	datagen, headers = multipart_encode({
		"info": info,
		"result": result,
	})
	out = '\r\n'.join(list(datagen))
	return send_file(io.BytesIO(out),
		mimetype=headers['Content-Type'])

if __name__ == "__main__":
    app.run(debug=True)
