#!/bin/bash

makeArrayString(){
	echo $1 | sed 's/[][]//g' | sed 's/\,/ /g'
}

outputArrayVar() {
	local array=$1[@]
	printf '%s\n' "${!array}" | jq -R . | jq -s . > /tmp/output/$2
}

mkdir -p $work_dir || exit 1
mkdir -p $genome_dir || exit 1

# Prepend output files with date and time
[ -n "$prepend_date" ] && current_date=$(date +"%Y%m%d_%H%M%S_")

files=($(makeArrayString $inputFiles))
bamSeen=false
for file in "${files[@]}"; do
	echo "working on $file"
	unquotedFile=$(echo $file | sed 's/\"//g')
	if [ -n "$custom_extension" ]; then
		extension=$custom_extension
	elif ! extension=$(echo ${unquotedFile} | grep -Eo '\.bam$|\.fastq\.gz$|\.fastq$|\.fq\.gz$|\.fq$'); then
		echo "ERROR: File type not supported by this Start widget, Supported file types are .bam, fastq.gz, .fastq, .fq.gz, and .fq"
		echo "You may bypass the Start widget check by entering a custom file extension"
		exit 1
	fi
	echo "extension is $extension"
	case "$extension" in
		.fastq.gz|.fastq|.fq.gz|.fq)
			fq=$(echo $extension | cut -c 2-)
			;;
		*)
			fq="fq"
			;;
	esac
	filename=$(basename -- "$unquotedFile")
	#use rsync instead of cp to not generate an error if file is already in workdir and to only clobber if file is different
	printf "rsync -aq $file $work_dir/$filename"
	eval "rsync -aq $file $work_dir/$filename"
	fileBase="$work_dir/$current_date${filename%.*}"
	if [[ $extension == ".bam" ]]; then
		#filenames for biobambam
		archive_files+=($work_dir/${filename%.*}.bam)
		bamSeen=true
		fastq1+=(${fileBase}_1.$fq)
		fastq2+=(${fileBase}_2.$fq)
		fastqO1+=(${fileBase}_o1.$fq)
		fastqO2+=(${fileBase}_o2.$fq)
		fastqs+=(${fileBase}_s.$fq)
		if [ -n "${pairedend}" ]; then
			#new filenames for bwa
			fastq+=(${fileBase}_1.$fq)
			fastq+=(${fileBase}_2.$fq)
		else
			fastq+=(${fileBase}_s.$fq)
		fi
	else
		#filenames for bwa
		fastq+=(${fileBase}.$fq)
		archive_files+=($work_dir/${filename%.*}.$fq)
	fi
	bams+=($work_dir/${filename%.*}.bam)
	cleanBams+=(${fileBase}_clean.bam)
	fastqc+=(${fileBase}'*.'$fq)
	hcVcf+=(${fileBase}.g.vcf)
	realignBams+=(${fileBase}_realign.bam)
	recalibrateBams+=(${fileBase}_realign_mark_dupes.bam)
done

# Pedigree file
if [ -n "$pedigree_files" ]; then
	echo $pedigree_files > /tmp/output/pedigree_files
	archive_files+=($pedigree_files)
fi

# GATK Haplotype caller
haplotype_caller=($work_dir/${current_date}sam.out.bam)
outputArrayVar haplotype_caller gatk_haplotype_out_bam

# GATK DB Import
db_file=$work_dir/${current_date}gatk_db
echo $db_file > /tmp/output/gatk_db_out

# GATK GVCF
gatk_gvcf_out_vcf=($work_dir/${current_date}combined.vcf)
outputArrayVar gatk_gvcf_out_vcf gatk_gvcf_out_vcf

# GATK CalculateGenotypePosteriors
refined_vcf=$work_dir/${current_date}combined_refined.vcf
echo $refined_vcf > /tmp/output/gatk_refined_out_vcf

# output delete files to cleanup
if [ -n "$prepend_date" ]; then
	delete_files=($work_dir/${current_date}'*')
else
	# this isn't a comprehensive list but the best we can do without the date/time stamp
	delete_files=(${cleanBams[@]} ${hcVcf[@]} ${realignBams[@]} ${recalibrateBams[@]} \
		${fastq1[@]} ${fastq2[@]} ${fastqO1[@]} ${fastqO2[@]} ${fastqs[@]} \
		${haplotype_caller[@]} $db_file ${gatk_gvcf_out_vcf[@]} $refined_vcf)
fi
archive_files+=(${delete_files[@]})

# output prefix to cleanup
if [ -n "$prepend_date" ]; then
	echo ${current_date}gdc_dna_seq > /tmp/output/archive_prefix
else
	echo $(date +"%Y%m%d_%H%M%S_")gdc_dna_seq > /tmp/output/archive_prefix
fi

outputArrayVar archive_files archive_files
outputArrayVar delete_files delete_files
outputArrayVar bams bamfiles
outputArrayVar cleanBams cleanbamfiles
outputArrayVar fastq fastqfiles
outputArrayVar fastqc fastqcfiles
outputArrayVar hcVcf hcvcffiles
outputArrayVar realignBams realignedfiles
outputArrayVar recalibrateBams recalibratebamfiles
if $bamSeen; then
	outputArrayVar fastq1 fastq1files
	outputArrayVar fastq2 fastq2files
	outputArrayVar fastqO1 fastqo1files
	outputArrayVar fastqO2 fastqo2files
	outputArrayVar fastqs fastqsfiles
else
	#skip biobambam if no bam files
	printf '1' > /tmp/output/bypassBiobambam
fi
