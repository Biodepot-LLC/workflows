#!/bin/bash
set -o pipefail

makeArrayString() {
	echo $1 | sed 's/[][]//g; s/\,/ /g'
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

# Prepend output files with date and time
[ -n "$prepend_date" ] && current_date=$(date +"%Y%m%d_%H%M%S_")

files=($(makeArrayString $input_normal_files))
files+=($(makeArrayString $input_tumor_files))
bamSeen=false
for file in "${files[@]}"; do
	echo "working on $file"
	unquoted=$(unquotedFile $file)
	if [ -n "$custom_extension" ]; then
		extension=$custom_extension
	elif ! extension=$(echo ${unquoted} | grep -Eo '\.bam$|\.fastq\.gz$|\.fastq$|\.fq\.gz$|\.fq$'); then
		echo "ERROR: File type not supported by this Start widget, Supported file types are .bam, fastq.gz, .fastq, .fq.gz, and .fq"
		echo "You may bypass the Start widget check by entering a custom file extension"
		exit 1
	fi
	echo "extension is $extension"
	case $extension in
		.fastq.gz|.fastq|.fq.gz|.fq)
			fq=$(echo $extension | cut -c 2-)
			;;
		*)
			fq='fq'
			;;
	esac
	filename=$(basename -- "$unquoted")
	# use rsync instead of cp to avoid an error if file is already in workdir and to only clobber if file is different
	cmd="rsync -aq $file $work_dir/$filename"
	echo $cmd
	eval $cmd
	fileBase="$work_dir/$current_date${filename%.*}"
	if [[ $extension == '.bam' ]]; then
		# filenames for biobambam
		bamSeen=true
		fastq1_files+=(${fileBase}_1.$fq)
		fastq2_files+=(${fileBase}_2.$fq)
		fastqo1_files+=(${fileBase}_o1.$fq)
		fastqo2_files+=(${fileBase}_o2.$fq)
		fastqs_files+=(${fileBase}_s.$fq)
		archive_files+=($work_dir/${filename%.*}.bam)
		if [ -n "${paired_end}" ]; then
			# filenames for bwa
			fastq_files+=(${fileBase}_1.$fq)
			fastq_files+=(${fileBase}_2.$fq)
		else
			fastq_files+=(${fileBase}_s.$fq)
		fi
	else
		# filenames for bwa
		fastq_files+=($work_dir/${filename%.*}.$fq)
		archive_files+=($work_dir/${filename%.*}.$fq)
	fi
	biobambam_files+=($work_dir/${filename%.*}.bam)
	clean_files+=(${fileBase}_clean.bam)
	fastqc_files+=(${fileBase}'*.'$fq)
	mark_dupes_metrics+=(${fileBase}_mark_dupes.metrics.txt)
	mark_dupes_outputs+=(${fileBase}_mark_dupes.bam)
	pindel_filter_files+=(${fileBase}_filter.bam)
	realigned_files+=(${fileBase}_realign.bam)
	realigned_indels_files+=(${fileBase}_realign_indels.bam)
done

# output normal mutect2 files
for file in "$(makeArrayString $input_normal_files)"; do
	unquoted=$(basename -- $(unquotedFile $file))
	fileBase="$work_dir/$current_date${unquoted%.*}"
	mutect2_normal_files+=(${fileBase}_clean.bam)
done

# output tumor mutect2/variant annotation/maf files
for file in "$(makeArrayString $input_tumor_files)"; do
	unquoted=$(basename -- $(unquotedFile $file))
	fileBase="$work_dir/$current_date${unquoted%.*}"
	coclean_intervals+=(${fileBase}_intervals.list)
	muse_call_files+=(${fileBase}_muse_calls)
	muse_sump_input_files+=(${fileBase}_muse_calls.MuSE.txt)
	muse_sump_output_files+=(${fileBase}_muse_calls.MuSE.txt.vcf)
	mutect2_tumor_files+=(${fileBase}_clean.bam)
	mutect2_variants_files+=(${fileBase}_mutect_variants.vcf)
	pindel_config_files+=(${fileBase}_pindel_config)
	pindel_prefix_files+=(${fileBase}_pindel_variants)
	pindel_variants_files+=(${fileBase}_pindel_variants.vcf)
	pindel_variants_sorted_files+=(${fileBase}_pindel_variants_sorted.vcf)
	pindel_variants_filtered_files+=(${fileBase}_pindel_variants_filtered.vcf)
	somatic_sniper_files+=(${fileBase}_somatic_sniper_snps.vcf)
    variant_input_files+=(${fileBase}_mutect_variants.vcf)
	variant_input_files+=(${fileBase}_pindel_variants_filtered.vcf)
	variant_input_files+=(${fileBase}_varscan_indel.Somatic.hc.vcf)
	variant_input_files+=(${fileBase}_varscan_snp.Somatic.hc.vcf)
	variant_input_files+=(${fileBase}_muse_calls.MuSE.txt.vcf)
	variant_input_files+=(${fileBase}_somatic_sniper_snps.vcf)
	variant_annotation_files+=(${fileBase}_mutect_variants.vep.vcf)
	variant_annotation_files+=(${fileBase}_pindel_variants_filtered.vep.vcf)
	variant_annotation_files+=(${fileBase}_varscan_indel.Somatic.hc.vep.vcf)
	variant_annotation_files+=(${fileBase}_varscan_snp.Somatic.hc.vep.vcf)
	variant_annotation_files+=(${fileBase}_muse_calls.MuSE.txt.vep.vcf)
	variant_annotation_files+=(${fileBase}_somatic_sniper_snps.vep.vcf)
	maf_files+=(${fileBase}_mutect_variants.maf)
	maf_files+=(${fileBase}_pindel_variants_filtered.maf)
	maf_files+=(${fileBase}_varscan_indel.Somatic.hc.maf)
	maf_files+=(${fileBase}_varscan_snp.Somatic.hc.maf)
	maf_files+=(${fileBase}_muse_calls.MuSE.txt.maf)
	maf_files+=(${fileBase}_somatic_sniper_snps.maf)
	varscan_pileup_files+=(${fileBase}_varscan_pileup.bam)
	varscan_snp_files+=(${fileBase}_varscan_snp.vcf)
	varscan_indel_files+=(${fileBase}_varscan_indel.vcf)
done

# output delete files to cleanup
if [ -n "$prepend_date" ]; then
	delete_files=($work_dir/${current_date}'*')
else
	# this isn't a comprehensive list but the best we can do without the date/time stamp
	delete_files=(${fastq1_files[@]} ${fastq2_files[@]} ${fastqo1_files[@]} ${fastqo2_files[@]} ${fastqs_files[@]} \
		${clean_files[@]} ${coclean_intervals[@]} ${mark_dupes_metrics[@]} ${mark_dupes_outputs[@]} \
		${pindel_filter_files[@]} ${realigned_files[@]} ${realigned_indels_files[@]} ${maf_files[@]} \
		${muse_sump_input_files[@]} ${muse_sump_output_files[@]} ${mutect2_variants_files[@]} \
		${pindel_config_files[@]} ${pindel_variants_files[@]} ${pindel_variants_sorted_files[@]} \
		${pindel_variants_filtered_files[@]} ${somatic_sniper_files[@]} ${variant_annotation_files[@]} ${variant_input_files[@]}\
		${varscan_pileup_files[@]} ${varscan_snp_files[@]} ${varscan_indel_files[@]})
fi
archive_files+=(${delete_files[@]})

# output prefix to cleanup
if [ -n "$prepend_date" ]; then
	echo ${current_date}gdc_dna_seq > /tmp/output/archive_prefix
else
	echo $(date +"%Y%m%d_%H%M%S_")gdc_dna_seq > /tmp/output/archive_prefix
fi

# output genome dictionary file
echo $genome_file | sed 's/fa$/dict/' > /tmp/output/genome_dict_file

outputArrayVar archive_files
outputArrayVar delete_files
outputArrayVar biobambam_files
outputArrayVar clean_files
outputArrayVar coclean_intervals
outputArrayVar fastq_files
outputArrayVar fastqc_files
outputArrayVar maf_files
outputArrayVar mark_dupes_metrics
outputArrayVar mark_dupes_outputs
outputArrayVar muse_call_files
outputArrayVar muse_sump_input_files
outputArrayVar muse_sump_output_files
outputArrayVar mutect2_normal_files
outputArrayVar mutect2_tumor_files
outputArrayVar mutect2_variants_files
outputArrayVar pindel_config_files
outputArrayVar pindel_filter_files
outputArrayVar pindel_prefix_files
outputArrayVar pindel_variants_files
outputArrayVar pindel_variants_sorted_files
outputArrayVar pindel_variants_filtered_files
outputArrayVar realigned_files
outputArrayVar realigned_indels_files
outputArrayVar somatic_sniper_files
outputArrayVar variant_annotation_files
outputArrayVar variant_input_files
outputArrayVar varscan_pileup_files
outputArrayVar varscan_snp_files
outputArrayVar varscan_indel_files

if $bamSeen; then
	outputArrayVar fastq1_files
	outputArrayVar fastq2_files
	outputArrayVar fastqo1_files
	outputArrayVar fastqo2_files
	outputArrayVar fastqs_files
else
	# skip biobambam if no bam files
	printf '1' > /tmp/output/bypass_biobambam
fi
