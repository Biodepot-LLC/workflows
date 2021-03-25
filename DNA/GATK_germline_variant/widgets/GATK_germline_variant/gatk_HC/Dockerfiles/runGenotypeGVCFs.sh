#!/bin/bash

putFlagInArray(){
 flags+=($(echo $1 | sed "s/[[\,]/$2/g" | sed "s/[]\"]//g"))
}
parseInputFile(){
	extension="${inputfile#*.}"
	case "$extension" in
		"g.vcf"|"g.vcf.gz"|"vcf"|"vcf.gz") 
			flags+=(" -V $inputfile " );;
		*) 
		flags+=(" -V gendb://$inputfile ");;
	esac
}
flags=($@)
parseInputFile

#gatk put flags multiple times for multiple values instead of putting multiple values after one flag
#bwb passes these flags as arrays in json format which need to be parsed
[ -z ${annotationgroup+x} ] || putFlagInArray $annotationgroup ' -G '


echo "gatk --java-options \"-Xmx4g\" GenotypeGVCFs ${flags[@]}"
gatk --java-options "-Xmx4g" GenotypeGVCFs ${flags[@]}
