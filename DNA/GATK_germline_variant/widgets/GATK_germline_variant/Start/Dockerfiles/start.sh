#!/bin/bash

makeArrayString(){
 echo $1 | sed 's/[][]//g' | sed 's/\,/ /g'
}


printenv

mkdir -p $work_dir || exit 1
mkdir -p $genome_dir || exit 1
# Variant Effect Predictor (DNA seq workflow) needs permissions set for UID 999
if [ -n "$vep_dir" ]; then
	mkdir -p $vep_dir || exit 1
	chown 999 $vep_dir
fi

files=($(makeArrayString $inputFiles))

for file in "${files[@]}"; do
  echo "working on $file"
  extension="${file#*.}"
  filename=$(basename -- "$file")
  fileBase="${filename%.*}"
  cleanBam+=($fileBase"_clean.bam")
done
printf '%s\n' "${cleanBam[@]}" | jq -R . | jq -s . > "/tmp/output/cleanfiles"


