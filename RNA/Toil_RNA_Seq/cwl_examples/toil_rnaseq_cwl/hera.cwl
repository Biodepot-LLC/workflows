cwlVersion: v1.0
class: CommandLineTool
label: Hera
baseCommand: docker
arguments: ["run"]
stdout: hera.cwl.txt
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
  docker_image_hera:
    type: string
    inputBinding:
      position: 3
  hera_method:
    type: string
    inputBinding:
      position: 4
  hera_index_dir:
    type: string
    inputBinding:
      position: 5
      prefix: -i
  trimmed_fastq_file_1:
    type: string
    inputBinding:
      position: 6
  trimmed_fastq_file_2:
    type: string
    inputBinding:
      position: 7
outputs:
  output:
    type: stdout
