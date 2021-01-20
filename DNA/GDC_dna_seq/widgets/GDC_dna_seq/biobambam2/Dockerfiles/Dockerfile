FROM ubuntu:18.04
LABEL maintainer=rgs1<rgs1@uw.edu>

# base utils to be used inside container
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      software-properties-common \
    && add-apt-repository -y ppa:gt1/biobambam2 \
    && add-apt-repository -y ppa:gt1/libmaus2 \
    && apt-get update \
    && apt-get install -y \
      biobambam2 \
    && apt-get purge -y software-properties-common \
    && apt-get autoremove -y --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root
