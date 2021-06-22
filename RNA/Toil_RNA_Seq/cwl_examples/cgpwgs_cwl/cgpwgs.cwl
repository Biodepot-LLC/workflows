class: CommandLineTool
id: "cgpwgs"
label: "CGP WGS analysis flow"
cwlVersion: v1.0
baseCommand: docker
arguments: ["run", "-v", "${PWD}:/data", "quay.io/wtsicgp/dockstore-cgpwgs:2.1.1"]
inputs:
  reference:
    type: File
    doc: "The core reference (fa, fai, dict) as tar.gz"
    inputBinding:
      prefix: -reference
      separate: true

  annot:
    type: File
    doc: "The VAGrENT cache files"
    inputBinding:
      prefix: -annot
      separate: true

  snv_indel:
    type: File
    doc: "Supporting files for SNV and INDEL analysis"
    inputBinding:
      prefix: -snv_indel
      separate: true

  cnv_sv:
    type: File
    doc: "Supporting files for CNV and SV analysis"
    inputBinding:
      prefix: -cnv_sv
      separate: true

  qcset:
    type: File
    doc: "Supporting files for QC tools"
    inputBinding:
      prefix: -qcset
      separate: true

  tumour:
    type: File
    secondaryFiles:
    - .bas
    doc: "Tumour BAM or CRAM file"
    inputBinding:
      prefix: -tumour
      separate: true

  tumourIdx:
    type: File
    doc: "Tumour alignment file index [bai|csi|crai]"
    inputBinding:
      prefix: -tidx
      separate: true

  normal:
    type: File
    secondaryFiles:
    - .bas
    doc: "Normal BAM or CRAM file"
    inputBinding:
      prefix: -normal
      separate: true

  normalIdx:
    type: File
    doc: "Normal alignment file index"
    inputBinding:
      prefix: -nidx
      separate: true

  exclude:
    type: string
    doc: "Contigs to block during indel analysis"
    inputBinding:
      prefix: -exclude
      separate: true
      shellQuote: true

  species:
    type: string?
    doc: "Species to apply if not found in BAM headers"
    default: ''
    inputBinding:
      prefix: -species
      separate: true
      shellQuote: true

  assembly:
    type: string?
    doc: "Assembly to apply if not found in BAM headers"
    default: ''
    inputBinding:
      prefix: -assembly
      separate: true
      shellQuote: true

  skipqc:
    type: boolean?
    doc: "Disable genotype and verifyBamID steps"
    inputBinding:
      prefix: -skipqc
      separate: true

  pindelcpu:
    type: int?
    doc: "Max cpus for pindel, ignores >8"
    default: 8
    inputBinding:
      prefix: -pindelcpu
      separate: true

  cavereads:
    type: int?
    doc: "Number of reads in a split section for CaVEMan"
    default: 350000
    inputBinding:
      prefix: -cavereads
      separate: true

  purity:
    type: float?
    doc: "Set the purity (rho) for ascat when default solution needs additional guidance. If set ploidy is also required."
    inputBinding:
      prefix: -pu
      separate: true

  ploidy:
    type: float?
    doc: "Set the ploidy (psi) for ascat when default solution needs additional guidance. If set purity is also required."
    inputBinding:
      prefix: -pi
      separate: true


outputs:
  run_params:
    type: File
    outputBinding:
      glob: run.params

  result_archive:
    type: File
    outputBinding:
      glob: WGS_*_vs_*.result.tar.gz

  # named like this so can be converted to a secondaryFile set once supported by dockstore cli
  timings:
    type: File
    outputBinding:
      glob: WGS_*_vs_*.timings.tar.gz

  global_time:
    type: File
    outputBinding:
      glob: WGS_*_vs_*.time
