FROM gcr.io/google.com/cloudsdktool/cloud-sdk:277.0.0-alpine
RUN apk update upgrade --no-cache && apk add jq bash musl-dev libgcc libgomp libstdc++  boost-filesystem
COPY w384/ /384/
COPY w96/ /96/
ENV NWELLS 96
COPY umisplit_gcpupload.sh /usr/local/bin/.
COPY runUploadSplitFiles.sh /usr/local/bin/.
COPY uploadSplitFiles.sh /usr/local/bin/.
