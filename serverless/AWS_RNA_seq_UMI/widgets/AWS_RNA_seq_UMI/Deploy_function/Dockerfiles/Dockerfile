FROM python:3.8.0-alpine3.10
ARG CLI_VERSION=1.16.272
RUN apk upgrade && apk add --no-cache bash zip jq
RUN pip install --upgrade pip && pip install --no-cache-dir awscli==$CLI_VERSION && \
    mkdir /root/.aws
RUN pip3 uninstall -y botocore boto3 && pip3 install botocore boto3
COPY deploy.py /usr/local/bin/deploy.py
