# tinytusk

A tiny C build server.

## requirements

Python 2.7 and Docker (boot2docker as well if on OSX).

## installing

```
source venv/bin/activate
pip install -r requirements.txt
docker build -t tinytusk docker/
```

updating packages

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

All editing is done in-browser. The browser will produce a tarball that is sent to a job API, returning a token. This token can be polled intermittently until the job is completed.

## license

MIT or ASL2
