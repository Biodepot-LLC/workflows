#!/bin/bash
name=$1
if [ -z $name ]; then
 name=somatic_sniper:test
fi
docker build -t somatic_sniper:temp -f Dockerfile-build .
docker run --rm -it -v ${PWD}:/data somatic_sniper:temp cp /usr/local/bin/bam-somaticsniper /data/.
docker build -t $name .
