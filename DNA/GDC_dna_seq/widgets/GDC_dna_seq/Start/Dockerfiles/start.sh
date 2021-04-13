#!/bin/bash

makeArrayString() {
	echo $1 | sed 's/[][]//g' | sed 's/\,/ /g'
}

outputArrayVar() {
	local array=$1[@]
	printf '%s\n' "${!array}" | jq -R . | jq -s . > "/tmp/output/$1"
}

unquotedFile() {
	echo $* | sed 's/\"//g'
}

mkdir -p $work_dir || exit 1
mkdir -p $genome_dir || exit 1
# Variant Effect Predictor
mkdir -p $vep_dir || exit 1

files=($(makeArrayString $input_normal_files))
files+=($(makeArrayString $input_tumor_files))
bamSeen=false
for file in "${files[@]}"; do
	echo "working on $file"
	unquoted=$(unquotedFile $file)
	extension="${unquoted#*.}"
	echo "extension is $extension"
	case "$extension" in
		"fastq"|"fastq.gz"|"fq.gz")
			fq=$extension
			;;
		*)
			fq="fq"
			;;
	esac
	filename=$(basename -- "$unquoted")
	# use rsync instead of cp to avoid an error if file is already in workdir and to only clobber if file is different
	cmd="rsync -aq $file $work_dir/$filename"
	echo $cmd
	eval $cmd
	fileBase="$work_dir/${filename%.*}"
	if [[ $extension == "bam" ]]; then
		# filenames for biobambam
		bamSeen=true
		fastq1_files+=(${fileBase}_1.$fq)
		fastq2_files+=(${fileBase}_2.$fq)
		fastqo1_files+=(${fileBase}_o1.$fq)
		fastqo2_files+=(${fileBase}_o2.$fq)
		fastqs_files+=(${fileBase}_s.$fq)
		if [ -n "${paired_end}" ]; then
			# filenames for bwa
			fastq_files+=(${fileBase}_1.$fq)
			fastq_files+=(${fileBase}_2.$fq)
		else
			fastq_files+=(${fileBase}_s.$fq)
		fi
	else
		# filenames for bwa
		fastq_files+=(${fileBase}.$fq)
	fi
	biobambam_files+=(${fileBase}.bam)
	clean_files+=(${fileBase}_clean.bam)
	fastqc_files+=(${fileBase}'*.'$fq)
	realigned_files+=(${fileBase}_realign.bam)
	realigned_indels_files+=(${fileBase}_realign_indels.bam)
	recalibrate_files+=(${fileBase}_realign_mark_dupes.bam)
	pindel_files+=(${fileBase}_filter.bam)
done

# output normal mutect2 files
for file in "$(makeArrayString $input_normal_files)"; do
	unquoted=$(unquotedFile $file)
	mutect2_normal_files+=(${unquoted%.*}_clean.bam)
done

# output tumor mutect2/variant annotation/maf files
for file in "$(makeArrayString $input_tumor_files)"; do
	unquoted=$(unquotedFile $file)
	mutect2_tumor_files+=(${unquoted%.*}_clean.bam)
	mutect2_variants_files+=(${unquoted%.*}_mutect_variants.vcf)
	variant_annotation_files+=(${unquoted%.*}_mutect_variants.vep.vcf)
	maf_files+=(${unquoted%.*}_mutect_variants.vep.vcf.maf)
done

# output genome dictionary file
echo $genome_file | sed 's/fa$/dict/' > /tmp/output/genome_dict_file

outputArrayVar biobambam_files
outputArrayVar clean_files
outputArrayVar fastq_files
outputArrayVar fastqc_files
outputArrayVar realigned_files
outputArrayVar realigned_indels_files
outputArrayVar recalibrate_files
outputArrayVar pindel_files
outputArrayVar mutect2_normal_files
outputArrayVar mutect2_tumor_files
outputArrayVar mutect2_variants_files
outputArrayVar variant_annotation_files
outputArrayVar maf_files

if $bamSeen; then
	outputArrayVar fastq1_files
	outputArrayVar fastq2_files
	outputArrayVar fastqo1_files
	outputArrayVar fastqo2_files
	outputArrayVar fastqs_files
else
	# skip biobambam if no bam files
	printf 'True' > /tmp/output/bypass_biobambam
fi
