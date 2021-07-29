import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWStart(OWBwBWidget):
    name = "Start"
    description = "Enter workflow parameters and start"
    priority = 1
    icon = getIconName(__file__,"start.png")
    want_main_area = False
    docker_image_name = "biodepot/gdc-mrna-start"
    docker_image_tag = "alpine_3.12.1__6334395c"
    outputs = [("work_dir",str),("genome_dir",str),("vep_dir",str),("genome_file",str),("gdc_credentials",str),("gdc_token",str),("clean_files",str),("fastq_files",str),("fastq1_files",str),("fastq2_files",str),("fastqo1_files",str),("fastqo2_files",str),("fastqs_files",str),("fastqc_files",str),("realigned_files",str),("realigned_indels_files",str),("pindel_filter_files",str),("genome_dict_file",str),("biobambam_files",str),("mutect2_normal_files",str),("mutect2_tumor_files",str),("mutect2_variants_files",str),("variant_input_files",str),("variant_annotation_files",str),("maf_files",str),("mark_dupes_outputs",str),("mark_dupes_metrics",str),("coclean_intervals",str),("somatic_sniper_files",str),("varscan_pileup_files",str),("varscan_snp_files",str),("varscan_indel_files",str),("muse_call_files",str),("muse_sump_input_files",str),("muse_sump_output_files",str),("pindel_config_files",str),("pindel_variants_files",str),("pindel_variants_sorted_files",str),("pindel_variants_filtered_files",str),("pindel_prefix_files",str),("archive_prefix",str),("archive_files",str),("delete_files",str),("cpu_threads",str),("bypass_biobambam",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    work_dir=pset(None)
    genome_dir=pset(None)
    vep_dir=pset(None)
    genome_file=pset(None)
    gdc_credentials=pset(None)
    gdc_token=pset(None)
    clean_files=pset([])
    fastq_files=pset([])
    fastq1_files=pset([])
    fastq2_files=pset([])
    fastqo1_files=pset([])
    fastqo2_files=pset([])
    fastqs_files=pset([])
    fastqc_files=pset([])
    paired_end=pset(True)
    realigned_files=pset([])
    realigned_indels_files=pset([])
    pindel_filter_files=pset([])
    genome_dict_file=pset(None)
    input_normal_files=pset([])
    input_tumor_files=pset([])
    biobambam_files=pset([])
    mutect2_normal_files=pset([])
    mutect2_tumor_files=pset([])
    mutect2_variants_files=pset([])
    variant_annotation_files=pset([])
    maf_files=pset([])
    mark_dupes_outputs=pset([])
    mark_dupes_metrics=pset([])
    coclean_intervals=pset(None)
    somatic_sniper_files=pset(None)
    prepend_date=pset(True)
    varscan_pileup_files=pset([])
    varscan_snp_files=pset([])
    varscan_indel_files=pset([])
    muse_call_files=pset([])
    muse_sump_input_files=pset([])
    muse_sump_output_files=pset([])
    pindel_config_files=pset([])
    pindel_variants_files=pset([])
    pindel_variants_sorted_files=pset([])
    pindel_variants_filtered_files=pset([])
    pindel_prefix_files=pset([])
    archive_prefix=pset(None)
    archive_files=pset([])
    delete_files=pset([])
    cpu_threads=pset(8)
    custom_extension=pset(None)
    bypass_biobambam=pset(False)
    variant_input_files=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Start")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"work_dir"):
            outputValue=getattr(self,"work_dir")
        self.send("work_dir", outputValue)
        outputValue=None
        if hasattr(self,"genome_dir"):
            outputValue=getattr(self,"genome_dir")
        self.send("genome_dir", outputValue)
        outputValue=None
        if hasattr(self,"vep_dir"):
            outputValue=getattr(self,"vep_dir")
        self.send("vep_dir", outputValue)
        outputValue=None
        if hasattr(self,"genome_file"):
            outputValue=getattr(self,"genome_file")
        self.send("genome_file", outputValue)
        outputValue=None
        if hasattr(self,"gdc_credentials"):
            outputValue=getattr(self,"gdc_credentials")
        self.send("gdc_credentials", outputValue)
        outputValue=None
        if hasattr(self,"gdc_token"):
            outputValue=getattr(self,"gdc_token")
        self.send("gdc_token", outputValue)
        outputValue=None
        if hasattr(self,"clean_files"):
            outputValue=getattr(self,"clean_files")
        self.send("clean_files", outputValue)
        outputValue=None
        if hasattr(self,"fastq_files"):
            outputValue=getattr(self,"fastq_files")
        self.send("fastq_files", outputValue)
        outputValue=None
        if hasattr(self,"fastq1_files"):
            outputValue=getattr(self,"fastq1_files")
        self.send("fastq1_files", outputValue)
        outputValue=None
        if hasattr(self,"fastq2_files"):
            outputValue=getattr(self,"fastq2_files")
        self.send("fastq2_files", outputValue)
        outputValue=None
        if hasattr(self,"fastqo1_files"):
            outputValue=getattr(self,"fastqo1_files")
        self.send("fastqo1_files", outputValue)
        outputValue=None
        if hasattr(self,"fastqo2_files"):
            outputValue=getattr(self,"fastqo2_files")
        self.send("fastqo2_files", outputValue)
        outputValue=None
        if hasattr(self,"fastqs_files"):
            outputValue=getattr(self,"fastqs_files")
        self.send("fastqs_files", outputValue)
        outputValue=None
        if hasattr(self,"fastqc_files"):
            outputValue=getattr(self,"fastqc_files")
        self.send("fastqc_files", outputValue)
        outputValue=None
        if hasattr(self,"realigned_files"):
            outputValue=getattr(self,"realigned_files")
        self.send("realigned_files", outputValue)
        outputValue=None
        if hasattr(self,"realigned_indels_files"):
            outputValue=getattr(self,"realigned_indels_files")
        self.send("realigned_indels_files", outputValue)
        outputValue=None
        if hasattr(self,"pindel_filter_files"):
            outputValue=getattr(self,"pindel_filter_files")
        self.send("pindel_filter_files", outputValue)
        outputValue=None
        if hasattr(self,"genome_dict_file"):
            outputValue=getattr(self,"genome_dict_file")
        self.send("genome_dict_file", outputValue)
        outputValue=None
        if hasattr(self,"biobambam_files"):
            outputValue=getattr(self,"biobambam_files")
        self.send("biobambam_files", outputValue)
        outputValue=None
        if hasattr(self,"mutect2_normal_files"):
            outputValue=getattr(self,"mutect2_normal_files")
        self.send("mutect2_normal_files", outputValue)
        outputValue=None
        if hasattr(self,"mutect2_tumor_files"):
            outputValue=getattr(self,"mutect2_tumor_files")
        self.send("mutect2_tumor_files", outputValue)
        outputValue=None
        if hasattr(self,"mutect2_variants_files"):
            outputValue=getattr(self,"mutect2_variants_files")
        self.send("mutect2_variants_files", outputValue)
        outputValue=None
        if hasattr(self,"variant_input_files"):
            outputValue=getattr(self,"variant_input_files")
        self.send("variant_input_files", outputValue)
        outputValue=None
        if hasattr(self,"variant_annotation_files"):
            outputValue=getattr(self,"variant_annotation_files")
        self.send("variant_annotation_files", outputValue)
        outputValue=None
        if hasattr(self,"maf_files"):
            outputValue=getattr(self,"maf_files")
        self.send("maf_files", outputValue)
        outputValue=None
        if hasattr(self,"mark_dupes_outputs"):
            outputValue=getattr(self,"mark_dupes_outputs")
        self.send("mark_dupes_outputs", outputValue)
        outputValue=None
        if hasattr(self,"mark_dupes_metrics"):
            outputValue=getattr(self,"mark_dupes_metrics")
        self.send("mark_dupes_metrics", outputValue)
        outputValue=None
        if hasattr(self,"coclean_intervals"):
            outputValue=getattr(self,"coclean_intervals")
        self.send("coclean_intervals", outputValue)
        outputValue=None
        if hasattr(self,"somatic_sniper_files"):
            outputValue=getattr(self,"somatic_sniper_files")
        self.send("somatic_sniper_files", outputValue)
        outputValue=None
        if hasattr(self,"varscan_pileup_files"):
            outputValue=getattr(self,"varscan_pileup_files")
        self.send("varscan_pileup_files", outputValue)
        outputValue=None
        if hasattr(self,"varscan_snp_files"):
            outputValue=getattr(self,"varscan_snp_files")
        self.send("varscan_snp_files", outputValue)
        outputValue=None
        if hasattr(self,"varscan_indel_files"):
            outputValue=getattr(self,"varscan_indel_files")
        self.send("varscan_indel_files", outputValue)
        outputValue=None
        if hasattr(self,"muse_call_files"):
            outputValue=getattr(self,"muse_call_files")
        self.send("muse_call_files", outputValue)
        outputValue=None
        if hasattr(self,"muse_sump_input_files"):
            outputValue=getattr(self,"muse_sump_input_files")
        self.send("muse_sump_input_files", outputValue)
        outputValue=None
        if hasattr(self,"muse_sump_output_files"):
            outputValue=getattr(self,"muse_sump_output_files")
        self.send("muse_sump_output_files", outputValue)
        outputValue=None
        if hasattr(self,"pindel_config_files"):
            outputValue=getattr(self,"pindel_config_files")
        self.send("pindel_config_files", outputValue)
        outputValue=None
        if hasattr(self,"pindel_variants_files"):
            outputValue=getattr(self,"pindel_variants_files")
        self.send("pindel_variants_files", outputValue)
        outputValue=None
        if hasattr(self,"pindel_variants_sorted_files"):
            outputValue=getattr(self,"pindel_variants_sorted_files")
        self.send("pindel_variants_sorted_files", outputValue)
        outputValue=None
        if hasattr(self,"pindel_variants_filtered_files"):
            outputValue=getattr(self,"pindel_variants_filtered_files")
        self.send("pindel_variants_filtered_files", outputValue)
        outputValue=None
        if hasattr(self,"pindel_prefix_files"):
            outputValue=getattr(self,"pindel_prefix_files")
        self.send("pindel_prefix_files", outputValue)
        outputValue=None
        if hasattr(self,"archive_prefix"):
            outputValue=getattr(self,"archive_prefix")
        self.send("archive_prefix", outputValue)
        outputValue=None
        if hasattr(self,"archive_files"):
            outputValue=getattr(self,"archive_files")
        self.send("archive_files", outputValue)
        outputValue=None
        if hasattr(self,"delete_files"):
            outputValue=getattr(self,"delete_files")
        self.send("delete_files", outputValue)
        outputValue=None
        if hasattr(self,"cpu_threads"):
            outputValue=getattr(self,"cpu_threads")
        self.send("cpu_threads", outputValue)
        outputValue=None
        if hasattr(self,"bypass_biobambam"):
            outputValue=getattr(self,"bypass_biobambam")
        self.send("bypass_biobambam", outputValue)
