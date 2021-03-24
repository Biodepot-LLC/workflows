cwlVersion: v1.0
class: CommandLineTool
label: RSem
baseCommand: docker
arguments: ["run"]
stdout: rsem.cwl.txt
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
  docker_image_rsem:
    type: string
    inputBinding:
      position: 3
  is_paired:
    type: string
    inputBinding:
      position: 4
  has_qualities:
    type: string
    inputBinding:
      position: 5
  threads:
    type: int
    inputBinding:
      position: 6
      prefix: -p
  probability:
    type: float
    inputBinding:
      position: 7
      prefix: --forward-prob
  seed_len:
    type: int
    inputBinding:
      position: 8
      prefix: --seed-length
  frag_len_mean:
    type: float
    inputBinding:
      position: 9
      prefix: --fragment-length-mean
  rsem_bam:
    type: string
    inputBinding:
      position: 10
      prefix: --bam
  rsem_header_path:
    type: string
    inputBinding:
      position: 11
  rsem_method:
    type: string
    inputBinding:
      position: 12
outputs:
  output:
    type: stdout
