# tinytusk

A tiny C build server.

## requirements

* Python 2.7
* Docker (boot2docker as well if on OSX)
* Browserify (`npm install -g browserify`)

## installing

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
docker build -t tinytusk ./docker/
npm install --prefix ./browser
```

when changing `browser/` code

```
browserify browser/index.js -o static/ide.js
```

when updating/adding python packages

```
pip freeze > requirements.txt
```

## running

```
source venv/bin/activate
python server.py
```

and open http://127.0.0.1:5000/

## structure

All editing is done in-browser. The browser IDE produces a tarball that is sent to a job API:

* `/api/test` &mdash; returns a multipart message of build errors/warnings and 
the stdout+stderr of the application
* `/api/build` &mdash; returns a multipart message of build errors/warnings and the binary of the application (Linux, 64-bit)

## license

MIT or ASL2
