FROM python:3.8.0-alpine3.10
ARG CLI_VERSION=1.16.272
RUN apk upgrade && apk add --no-cache nano bash zip findutils
RUN pip install --upgrade pip && pip install --no-cache-dir awscli==$CLI_VERSION && \
    mkdir /root/.aws
RUN apk update upgrade --no-cache && apk add jq musl-dev libgcc libgomp libstdc++  boost-filesystem
COPY w384/ /384/
COPY w96/ /96/
ENV NWELLS 96
COPY umisplit_awsupload.sh /usr/local/bin/.
COPY runUploadSplitFiles.sh /usr/local/bin/.
COPY uploadSplitFiles.sh /usr/local/bin/.
