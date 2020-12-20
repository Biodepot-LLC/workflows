FROM python:3.8.0-alpine3.10
RUN apk upgrade && apk add --no-cache build-base libffi-dev libressl-dev && \
    pip install --upgrade pip && pip install --no-cache-dir  google-cloud-storage google-cloud-pubsub && \
    apk del build-base && apk add --no-cache libgomp libgcc libstdc++
COPY setupGoogle.py /usr/local/bin/setupGoogle.py
COPY invokeGoogle.py /usr/local/bin/invokeGoogle.py

