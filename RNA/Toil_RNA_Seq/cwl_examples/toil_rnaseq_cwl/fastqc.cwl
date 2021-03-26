cwlVersion: v1.0
class: CommandLineTool
label: FastQC
baseCommand: docker
arguments: ["run"]
stdout: fastqc.cwl.txt
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
  docker_image_fastqc:
    type: string
    inputBinding:
      position: 3
  threads:
    type: int
    inputBinding:
      position: 4
      prefix: -t
  trimmed_fastq_file_1:
    type: string
    inputBinding:
      position: 5
  trimmed_fastq_file_2:
    type: string
    inputBinding:
      position: 6
outputs:
  output:
    type: stdout
