FROM python:3.8.0-alpine3.10
RUN apk upgrade && apk add --no-cache build-base libffi-dev libressl-dev && \
    pip install --upgrade pip && pip install --no-cache-dir  google-cloud-storage && \
    apk del build-base && apk add --no-cache libgcc libstdc++
COPY create.py /usr/local/bin/create.py

