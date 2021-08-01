cwlVersion: v1.0
class: CommandLineTool
label: STAR
baseCommand: docker
arguments: ["run"]
stdout: star.cwl.txt
inputs:
  volume_home:
    type: string
    inputBinding:
      position: 1
      prefix: -v
  volume_docker:
    type: string
    inputBinding:
      position: 2
      prefix: -v
  docker_image_star:
    type: string
    inputBinding:
      position: 3
  star_index_dir:
    type: string
    inputBinding:
      position: 4
      prefix: --genomeDir
  threads:
    type: int
    inputBinding:
      position: 5
      prefix: --runThreadN
  output_prefix:
    type: string
    inputBinding:
      position: 6
      prefix: --outFileNamePrefix
  quant_mode:
    type: string
    inputBinding:
      position: 7
      prefix: --quantMode
  read_files:
    type: string
    inputBinding:
      position: 8
  trimmed_fastq_file_1:
    type: string
    inputBinding:
      position: 9
  trimmed_fastq_file_2:
    type: string
    inputBinding:
      position: 9
outputs:
  output:
    type: stdout
