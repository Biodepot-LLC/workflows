#!/bin/bash

makeArrayString() {
	echo $1 | sed 's/[][]//g' | sed 's/\,/ /g'
}

outputArrayVar() {
	local array=$1[@]
	printf '%s\n' "${!array}" | jq -R . | jq -s . > "/tmp/output/$2"
}

mkdir -p $work_dir || exit 1
mkdir -p $genome_dir || exit 1
# Variant Effect Predictor (DNA seq workflow) needs permissions set for UID 999
if [ -n "$vep_dir" ]; then
	mkdir -p $vep_dir || exit 1
	chown 999 $vep_dir
fi

files=($(makeArrayString $input_files))
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
	cmd="rsync -aq $file $work_dir/$filename"
	echo $cmd
	eval $cmd
	fileBase="$work_dir/${filename%.*}"
	if [[ $extension == "bam" ]]; then
		#filenames for biobambam
		bamSeen=true
		fastq1+=(${fileBase}_1.$fq)
		fastq2+=(${fileBase}_2.$fq)
		fastqO1+=(${fileBase}_o1.$fq)
		fastqO2+=(${fileBase}_o2.$fq)
		fastqs+=(${fileBase}.$fq)
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
	cleanBams+=(${fileBase}_clean.bam)
	fastqc+=(${fileBase}'*.'$fq)
	realignBams+=(${fileBase}_realign.bam)
	realignIndelsBams+=(${fileBase}_realign_indels.bam)
	recalibrateBams+=(${fileBase}_realign_mark_dupes.bam)
	pindelFilterBams+=(${fileBase}_filter.bam)
done
# output genome dictionary file
echo $genome_file | sed 's/fa$/dict/' > /tmp/output/genome_dict_file

outputArrayVar cleanBams clean_files
outputArrayVar fastq fastq_files
outputArrayVar fastqc fastqc_files
outputArrayVar realignBams realigned_files
outputArrayVar realignIndelsBams realigned_indels_files
outputArrayVar recalibrateBams recalibrate_files
outputArrayVar pindelFilterBams pindel_files
if $bamSeen; then
	outputArrayVar fastq1 fastq1_files
	outputArrayVar fastq2 fastq2_files
	outputArrayVar fastqO1 fastqo1_files
	outputArrayVar fastqO2 fastqo2_files
	outputArrayVar fastqs fastqs_files
else
	#skip biobambam if no bam files
	printf 'True' > /tmp/output/bypass_biobambam
fi
