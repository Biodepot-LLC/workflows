#!/bin/bash

makeArrayString(){
 echo $1 | sed 's/[][]//g' | sed 's/\,/ /g'
}
putFlagInArray(){
 flags+=($(echo $1 | sed "s/[[\,]/$2/g" | sed "s/[]\"]//g"))
}
parseInputFiles(){
	files=($(makeArrayString $inputfiles))
	for file in "${files[@]}"; do
		unquotedFile=$(echo $file | sed 's/\"//g')
		extension="${unquotedFile#*.}"
		case "$extension" in
			"g.vcf"|"g.vcf.gz"|"vcf"|"vcf.gz") 
				flags+=(" -V $unquotedFile" );;
			*) 
			flags+=(" --sample-name-map $unquotedFile ");;
		esac
	done
}
flags=($@)
parseInputFiles
[ -n $overwrite ] && [ -d $outputfile ] && rm -r "$outputfile"

echo "gatk --java-options \"-Xmx4g\" GenomicsDBImport ${flags[@]}"
gatk --java-options "-Xmx4g" GenomicsDBImport ${flags[@]}



