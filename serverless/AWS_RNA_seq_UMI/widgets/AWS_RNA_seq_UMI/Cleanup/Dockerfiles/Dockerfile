FROM python:3.8.0-alpine3.10
ARG CLI_VERSION=1.18.105
ARG BOTO_VERSION=1.17.28
RUN apk upgrade && apk add --no-cache bash zip jq
RUN pip install --upgrade pip && pip install --no-cache-dir awscli==$CLI_VERSION && mkdir /root/.aws
#RUN pip3 install botocore==$BOTO_VERSION boto3
COPY cleanup_lambda.sh /usr/local/bin/cleanup_lambda.sh
