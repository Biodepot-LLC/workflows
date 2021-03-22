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
bamSeen=0
for file in "${files[@]}"; do
  echo "working on $file"
  unquotedFile=$(echo $file | sed 's/\"//g')
  extension="${unquotedFile#*.}" 
  echo "extension is $extension"
  case extension in
	fastq|fastq.gz|fq.gz) 
		fq=$extension;;
	*) 
		fq="fq";;
  esac
  filename=$(basename -- "$unquotedFile")
  #use rsync instead of cp to not generate an error if file is already in workdir and to only clobber if file is different
  printf "rsync -aq $file $work_dir/$filename"
  eval "rsync -aq $file $work_dir/$filename"
  fileBase="$work_dir/${filename%.*}"
  if [[ $extension == "bam" ]]; then
        #filenames for biobambam
		fastqs+=($fileBase".$fq")
		fastq1+=($fileBase"_1.$fq")
		fastq2+=($fileBase"_2.$fq")
		fastqO1+=($fileBase"_o1.$fq")
		fastqO2+=($fileBase"_o2.$fq")	
		bamSeen=1
	if [ -n ${pairedend+x} ]; then	
		#new filenames for bwa
		fastq+=($fileBase"_1.$fq")
		fastq+=($fileBase"_2.$fq")
	else
		fastq+=($fileBase".$fq")
	fi	
 else
	#filenames for bwa
	fastq+=($fileBase".$fq")
 fi
 bams+=($fileBase".bam")
 realignBams+=($fileBase"_realign.bam")
 cleanBams+=($fileBase"_clean.bam")
done


printf '%s\n' "${cleanBams[@]}" | jq -R . | jq -s . > "/tmp/output/cleanbamfiles"
printf '%s\n' "${fastq[@]}" | jq -R . | jq -s . > "/tmp/output/fastqfiles"
if [[ $extension == "bam" ]]; then
	printf '%s\n' "${bams[@]}" | jq -R . | jq -s . > "/tmp/output/bamfiles"
	printf '%s\n' "${realignBams[@]}" | jq -R . | jq -s . > "/tmp/output/realignedfiles"
	printf '%s\n' "${fastq1[@]}" | jq -R . | jq -s . > "/tmp/output/fastq1files"
	printf '%s\n' "${fastq2[@]}" | jq -R . | jq -s . > "/tmp/output/fastq2files"
	printf '%s\n' "${fastqO1[@]}" | jq -R . | jq -s . > "/tmp/output/fastqo1files"
	printf '%s\n' "${fastqO2[@]}" | jq -R . | jq -s . > "/tmp/output/fastqo2files"
	printf '%s\n' "${fastqs[@]}" | jq -R . | jq -s . > "/tmp/output/fastqsfiles"
else
	printf '%s\n' "${realignBams[@]}" | jq -R . | jq -s . > "/tmp/output/realignedfiles"
fi

#skip biobambam if no bam files
(($bamSeen)) || printf 'True' > "/tmp/output/bypassBiobambam"

