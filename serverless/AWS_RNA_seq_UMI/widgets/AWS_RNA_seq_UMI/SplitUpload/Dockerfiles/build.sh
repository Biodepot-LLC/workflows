#!/bin/bash
if [ $# -eq 0 ]; then
        name=biodepot/umisplit_awsupload:latest
else
    	name=$1
fi
docker build -t temp:build -f Dockerfile.build  .
#do not use $PWD for map - this will fail when run inside the bwb container as the volume names are not properly munge
# use docker cp
container=$(docker run --rm -it -d temp:build)
docker cp $container:/source/w96 .
docker cp $container:/source/w384 .
docker stop $container
docker image rm temp:build
docker build -t $name  -f Dockerfile .
rm -rf w96 w384
