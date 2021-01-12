FROM biodepot/gatk:4.1.9.0__openjdk_8-jre-alpine__cb1b2f17
MAINTAINER Hong Hung
RUN apk add --no-cache bash
ENV PATH=$PATH:/usr/local/bin/
COPY mark_dupes.sh /usr/local/bin/mark_dupes.sh
