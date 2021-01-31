FROM       python:3.8-slim
RUN        set -eux; \
    apt-get update
RUN        apt-get install ffmpeg -y
COPY       /src /src
RUN        pip install -r /src/requirements.txt
WORKDIR    /src
ENV        SHELL=/bin/bash
ENTRYPOINT ["python", "launcher.py"]