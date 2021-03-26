cwlVersion: v1.0
class: CommandLineTool
label: Kallisto
baseCommand: docker
arguments: ["run"]
stdout: kallisto.cwl.txt
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
  docker_image_kallisto:
    type: string
    inputBinding:
      position: 3
  kallisto_method:
    type: string
    inputBinding:
      position: 4
  kallisto_index_file:
    type: string
    inputBinding:
      position: 5
      prefix: -i
  threads:
    type: int
    inputBinding:
      position: 6
      prefix: -t
  kallisto_output:
    type: string
    inputBinding:
      position: 7
      prefix: -o
  bootstrap_samples:
    type: int
    inputBinding:
      position: 8
      prefix: -b
  fusion:
    type: string
    inputBinding:
      position: 9
  trimmed_fastq_file_1:
    type: string
    inputBinding:
      position: 10
  trimmed_fastq_file_2:
    type: string
    inputBinding:
      position: 11
outputs:
  output:
    type: stdout
