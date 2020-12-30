#!/bin/bash
name=$1
if [ -z $name ]; then
 name=varscan:test
fi
docker run --rm -it -v $PWD:/data biodepot/bwa-samtools:gdcalign__alpine_3.12__10034cca cp /usr/local/bin/samtools /data/.
docker build -t $name .
