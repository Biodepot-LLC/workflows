#!/bin/bash

putFlagInArray(){
 flags+=($(echo $1 | sed "s/[[\,]/$2/g" | sed "s/[]\"]//g"))
}
flags=($@)

#gatk put flags multiple times for multiple values instead of putting multiple values after one flag
#bwb passes these flags as arrays in json format which need to be parsed
[ -z ${annotationgroup+x} ] || putFlagInArray $annotationgroup ' -G '
[ -z ${annotation+x} ] || putFlagInArray $annotation ' --annotation '

echo "gatk --java-options \"-Xmx4g\" HaplotypeCaller ${flags[@]}"
gatk --java-options "-Xmx4g" HaplotypeCaller ${flags[@]}
