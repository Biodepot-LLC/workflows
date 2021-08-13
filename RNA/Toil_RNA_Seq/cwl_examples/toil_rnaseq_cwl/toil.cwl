cwlVersion: v1.0
class: Workflow
requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}
  ShellCommandRequirement: {}
label: Toil RNA-Seq
inputs:
  volume_home: string
  volume_docker: string
  docker_image_cutadapt: string
  docker_image_fastqc: string
  docker_image_hera: string
  docker_image_kallisto: string
  docker_image_star: string
  docker_image_rsem: string
  p_a: string
  p_m: int
  p_A: string
  fastq_file_1: string
  fastq_file_2: string
  trimmed_fastq_file_1: string
  trimmed_fastq_file_2: string
  threads: int
  hera_method: string
  hera_index_dir: string
  kallisto_method: string
  kallisto_index_file: string
  kallisto_output: string
  bootstrap_samples: int
  fusion: string
  star_index_dir: string
  star_quant_mode: string
  quant_mode: string
  output_prefix: string
  read_files: string
  is_paired: string
  has_qualities: string
  probability: float
  seed_len: int
  frag_len_mean: float
  rsem_bam: string
  rsem_header_path: string
  rsem_method: string
outputs: #[]
  output_cutadapt:
    type: File
    outputSource: cutadapt/output
  output_fastqc:
    type: File
    outputSource: fastqc/output
  output_hera:
    type: File
    outputSource: hera/output
  output_kallisto:
    type: File
    outputSource: kallisto/output
  output_star:
    type: File
    outputSource: star/output
  output_rsem:
    type: File
    outputSource: rsem/output
steps:
  cutadapt:
    run: cutadapt.cwl
    in:
      volume_home: volume_home
      volume_docker: volume_docker
      docker_image_cutadapt: docker_image_cutadapt
      p_a: p_a
      p_m: p_m
      p_A: p_A
      fastq_file_1: fastq_file_1
      fastq_file_2: fastq_file_2
      trimmed_fastq_file_1: trimmed_fastq_file_1
      trimmed_fastq_file_2: trimmed_fastq_file_2
    out:
      [output]
  fastqc:
    run: fastqc.cwl
    in:
      input_file: cutadapt/output
      volume_home: volume_home
      volume_docker: volume_docker
      docker_image_fastqc: docker_image_fastqc
      threads: threads
      trimmed_fastq_file_1: trimmed_fastq_file_1
      trimmed_fastq_file_2: trimmed_fastq_file_2
    out:
      [output]
  hera:
    run: hera.cwl
    in:
      input_file: cutadapt/output
      volume_home: volume_home
      volume_docker: volume_docker
      docker_image_hera: docker_image_hera
      hera_method: hera_method
      hera_index_dir: hera_index_dir
      trimmed_fastq_file_1: trimmed_fastq_file_1
      trimmed_fastq_file_2: trimmed_fastq_file_2
    out:
      [output]
  kallisto:
    run: kallisto.cwl
    in:
      input_file: cutadapt/output
      volume_home: volume_home
      volume_docker: volume_docker
      docker_image_kallisto: docker_image_kallisto
      kallisto_method: kallisto_method
      kallisto_index_file: kallisto_index_file
      threads: threads
      kallisto_output: kallisto_output
      bootstrap_samples: bootstrap_samples
      fusion: fusion
      trimmed_fastq_file_1: trimmed_fastq_file_1
      trimmed_fastq_file_2: trimmed_fastq_file_2
    out:
      [output]
  star:
    run: star.cwl
    in:
      input_file: cutadapt/output
      volume_home: volume_home
      volume_docker: volume_docker
      docker_image_star: docker_image_star
      star_index_dir: star_index_dir
      star_quant_mode: star_quant_mode
      quant_mode: quant_mode
      threads: threads
      output_prefix: output_prefix
      read_files: read_files
      trimmed_fastq_file_1: trimmed_fastq_file_1
      trimmed_fastq_file_2: trimmed_fastq_file_2
    out:
      [output]
  rsem:
    run: rsem.cwl
    in:
      input_file: star/output
      volume_home: volume_home
      volume_docker: volume_docker
      docker_image_rsem: docker_image_rsem
      is_paired: is_paired
      has_qualities: has_qualities
      threads: threads
      probability: probability
      seed_len: seed_len
      frag_len_mean: frag_len_mean
      rsem_bam: rsem_bam
      rsem_header_path: rsem_header_path
      rsem_method: rsem_method
    out:
      [output]




