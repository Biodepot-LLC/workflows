workflow toil_rnaseq
{
  String volume_home
  String volume_docker
  String docker_image_cutadapt
  String docker_image_fastqc
  String docker_image_hera
  String docker_image_star
  String docker_image_rsem
  String threads
  String a
  Int m
  String fastq_file_1
  String fastq_file_2
  String trimmed_fastq_file_1
  String trimmed_fastq_file_2
  
  String hera_method
  String hera_index_dir
  
  String kallisto_method
  String kallisto_index_file
  String kallisto_output
  Int bootstrap_samples
  String fusion
  
  String star_index_dir
  String output_prefix
  String read_files
  
  String is_paired
  String has_qualities
  Float probability
  Int seed_len
  Float frag_len_mean
  String rsem_bam
  String rsem_header_path
  String rsem_method
  
	call cutadapt { input: 
    volume_home=volume_home,
    volume_docker=volume_docker,
    docker_image=docker_image_cutadapt,
    a=a,
    m=m,
    trimmed_fastq_file_1=trimmed_fastq_file_1,
    trimmed_fastq_file_2=trimmed_fastq_file_2,
    fastq_file_1=fastq_file_1,
    fastq_file_2=fastq_file_2
  }
  
  call fastqc { input: 
    volume_home=volume_home,
    volume_docker=volume_docker,
    docker_image=docker_image_fastqc,
    threads=threads,
    trimmed_fastq_file_1=trimmed_fastq_file_1,
    trimmed_fastq_file_2=trimmed_fastq_file_2
  }
  
  call hera { input: 
    volume_home=volume_home,
    volume_docker=volume_docker,
    docker_image=docker_image_hera,
    method=hera_method,
    index_dir=hera_index_dir,
    trimmed_fastq_file_1=trimmed_fastq_file_1,
    trimmed_fastq_file_2=trimmed_fastq_file_2
  }
  
  call kallisto { input: 
    volume_home=volume_home,
    volume_docker=volume_docker,
    docker_image=docker_image_hera,
    method=kallisto_method,
    index_file=kallisto_index_file,
    threads=threads,
    kallisto_output=kallisto_output,
    bootstrap_samples=bootstrap_samples,
    fusion=fusion,
    trimmed_fastq_file_1=trimmed_fastq_file_1,
    trimmed_fastq_file_2=trimmed_fastq_file_2
  }
  
  call star { input: 
    volume_home=volume_home,
    volume_docker=volume_docker,
    docker_image=docker_image_star,
    index_dir=star_index_dir,
    threads=threads,
    output_prefix=output_prefix,
    read_files=read_files,
    trimmed_fastq_file_1=trimmed_fastq_file_1,
    trimmed_fastq_file_2=trimmed_fastq_file_2
  }
  
  call rsem { input: 
    volume_home=volume_home,
    volume_docker=volume_docker,
    docker_image=docker_image_rsem,
    
    is_paired=is_paired,
    has_qualities=has_qualities,
    threads=threads,
    probability=probability,
    seed_len=seed_len,
    frag_len_mean=frag_len_mean,
    rsem_bam=rsem_bam,
    rsem_header_path=rsem_header_path,
    rsem_method=rsem_method
  }
}

task cutadapt
{
	String volume_home
  String volume_docker
  String docker_image
  String a
  Int m
  String trimmed_fastq_file_1
  String trimmed_fastq_file_2
  String fastq_file_1
  String fastq_file_2
  
	command
  {
    docker run -v ${volume_home} -v ${volume_docker} ${docker_image} -a ${a} -m ${m} -A ${a} -o ${trimmed_fastq_file_1} -p ${trimmed_fastq_file_2} ${fastq_file_1} ${fastq_file_2}
  }
}

task fastqc
{
	String volume_home
  String volume_docker
  String docker_image
  Int threads
  String trimmed_fastq_file_1
  String trimmed_fastq_file_2
  
	command
  {
    docker run -v ${volume_home} -v ${volume_docker} ${docker_image} -t ${threads} ${trimmed_fastq_file_1} ${trimmed_fastq_file_2}
  }
}

task hera
{
	String volume_home
  String volume_docker
  String docker_image
  String method
  String index_dir
  String trimmed_fastq_file_1
  String trimmed_fastq_file_2
  
	command
  {
    docker run -v ${volume_home} -v ${volume_docker} ${docker_image} ${method} -i ${index_dir} ${trimmed_fastq_file_1} ${trimmed_fastq_file_2}
  }
}

task kallisto
{
	String volume_home
  String volume_docker
  String docker_image
  String method
  String index_file
  Int threads
  String kallisto_output
  Int bootstrap_samples
  String fusion
  String trimmed_fastq_file_1
  String trimmed_fastq_file_2
  
	command
  {
    docker run -v ${volume_home} -v ${volume_docker} ${docker_image} ${method} -i ${index_file} -t ${threads} -o ${kallisto_output} -b ${bootstrap_samples} ${fusion} ${trimmed_fastq_file_1} ${trimmed_fastq_file_2}
  }
}

task star
{
	String volume_home
  String volume_docker
  String docker_image
  String index_dir
  Int threads
  String output_prefix
  String read_files
  String trimmed_fastq_file_1
  String trimmed_fastq_file_2
  
	command
  {
    docker run -v ${volume_home} -v ${volume_docker} ${docker_image} --genomeDir ${index_dir} --runThreadN ${threads} --outFileNamePrefix ${output_prefix} ${read_files} ${trimmed_fastq_file_1} ${trimmed_fastq_file_2}
  }
}

task rsem
{
	String volume_home
  String volume_docker
  String docker_image
  
  String is_paired
  String has_qualities
  Int threads
  Float probability
  Int seed_len
  Float frag_len_mean
  String rsem_bam
  String rsem_header_path
  String rsem_method
  
	command
  {
    docker run -v ${volume_home} -v ${volume_docker} ${docker_image} ${is_paired} ${has_qualities} -p ${threads} --forward-prob ${probability} --seed-length ${seed_len} --fragment-length-mean ${frag_len_mean} --bam ${rsem_bam} ${rsem_header_path} ${rsem_method}
  }
}




