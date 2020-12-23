From ubuntu:14.04
MAINTAINER Ling-Hong Hung
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential \
	python2.7-dev \
	python-numpy \
	python-matplotlib \
	python-pip \
    && pip install "HTSeq==0.6.1" \
    && apt-get remove -y build-essential python-pip python2.7-dev \
    && apt-get clean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
