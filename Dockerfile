FROM python:alpine

WORKDIR /src
RUN apk add --no-cache --virtual \
    .pynacl_deps build-base ffmpeg libffi-dev python3-dev opus
COPY /src /src
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
