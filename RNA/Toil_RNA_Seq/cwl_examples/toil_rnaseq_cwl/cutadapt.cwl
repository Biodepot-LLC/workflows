cwlVersion: v1.0
class: CommandLineTool
label: CutAdapt
baseCommand: docker
arguments: ["run"]
stdout: cutadapt.cwl.txt
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
  docker_image_cutadapt:
    type: string
    inputBinding:
      position: 3
  p_a:
    type: string
    inputBinding:
      position: 4
      prefix: -a
  p_m:
    type: int
    inputBinding:
      position: 5
      prefix: -m
  p_A:
    type: string
    inputBinding:
      position: 6
      prefix: -A
  trimmed_fastq_file_1:
    type: string
    inputBinding:
      position: 7
      prefix: -o
  trimmed_fastq_file_2:
    type: string
    inputBinding:
      position: 8
      prefix: -p
  fastq_file_1:
    type: string
    inputBinding:
      position: 9
  fastq_file_2:
    type: string
    inputBinding:
      position: 10
outputs:
  output:
    type: stdout
