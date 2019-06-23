## FreemedAttendence-API
Freemed Attendence API based on Python Flask

## Install
This repository strongly recommend to use linux platform when develope.
On other OS, it's not tested so there will be risk of unexpected errors.
- Linux
```bash
$ pip install requirements_linux.txt
```

- Others
```bash
Install pytorch appropriate your hardware and OS. 
$ pip install requirements_others.txt
```

## Deploy with docker
```bash
$ docker build . -t attendence-api
$ docker run -dit -p 9000:9000 attendence-api
```

## Run API server
```bash
$ sh ./scripts/runserver.sh
```
or
```bash
$ gunicorn --bind 0.0.0.0:9000 -w 1 api.wsgi:app
```

## API documentation 
FaceDetection API : [doc](./docs/api/facedetection_api.md)
