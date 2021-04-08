#!/bin/bash

makeArrayString(){
	echo $1 | sed 's/[][]//g' | sed 's/\,/ /g'
}

outputArrayVar() {
	local array=$1[@]
	printf '%s\n' "${!array}" | jq -R . | jq -s . > "/tmp/output/$2"
}

#printenv

mkdir -p $work_dir || exit 1
mkdir -p $genome_dir || exit 1

files=($(makeArrayString $inputFiles))
bamSeen=false
for file in "${files[@]}"; do
	echo "working on $file"
	unquotedFile=$(echo $file | sed 's/\"//g')
	extension="${unquotedFile#*.}"
	echo "extension is $extension"
	case "$extension" in
		"fastq"|"fastq.gz"|"fq.gz")
			fq=$extension
			;;
		*)
			fq="fq"
			;;
	esac
	filename=$(basename -- "$unquotedFile")
	#use rsync instead of cp to not generate an error if file is already in workdir and to only clobber if file is different
	printf "rsync -aq $file $work_dir/$filename"
	eval "rsync -aq $file $work_dir/$filename"
	fileBase="$work_dir/${filename%.*}"
	if [[ $extension == "bam" ]]; then
		#filenames for biobambam
		fastqs+=(${fileBase}.$fq)
		fastq1+=(${fileBase}_1.$fq)
		fastq2+=(${fileBase}_2.$fq)
		fastqO1+=(${fileBase}_o1.$fq)
		fastqO2+=(${fileBase}_o2.$fq)
		bamSeen=true
		if [ -n ${pairedend+x} ]; then
			#new filenames for bwa
			fastq+=(${fileBase}_1.$fq)
			fastq+=(${fileBase}_2.$fq)
		else
			fastq+=(${fileBase}.$fq)
		fi
	else
		#filenames for bwa
		fastq+=(${fileBase}.$fq)
	fi
	fastqc+=(${fileBase}'*.'$fq)
	bams+=(${fileBase}.bam)
	realignBams+=(${fileBase}_realign.bam)
	cleanBams+=(${fileBase}_clean.bam)
	recalibrateBams+=(${fileBase}_realign_mark_dupes.bam)
	hcVcf+=(${fileBase}.g.vcf)
done

outputArrayVar realignBams realignedfiles
outputArrayVar cleanBams cleanbamfiles
outputArrayVar recalibrateBams recalibratebamfiles
outputArrayVar fastq fastqfiles
outputArrayVar fastqc fastqcfiles
outputArrayVar hcVcf hcvcffiles
if $bamSeen; then
	outputArrayVar bams bamfiles
	outputArrayVar fastq1 fastq1files
	outputArrayVar fastq2 fastq2files
	outputArrayVar fastqO1 fastqo1files
	outputArrayVar fastqO2 fastqo2files
	outputArrayVar fastqs fastqsfiles
else
	#skip biobambam if no bam files
	printf 'True' > "/tmp/output/bypassBiobambam"
fi
