FROM alpine:3.11.3
RUN apk update upgrade --no-cache && apk add bash musl-dev libgcc libgomp libstdc++  boost-filesystem
COPY w384/ /384/
COPY w96/ /96/
ADD start.sh /usr/local/bin/start.sh
ENV NWELLS 96
ENTRYPOINT ["start.sh"]

