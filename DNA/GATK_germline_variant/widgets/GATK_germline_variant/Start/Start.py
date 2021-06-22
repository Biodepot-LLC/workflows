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
    docker_image_name = "biodepot/gdc-gatk-germline-variant_start"
    docker_image_tag = "alpine_3.12.1__2d9947ef"
    outputs = [("work_dir",str),("genome_dir",str),("inputFiles",str),("genomefile",str),("cleanbamfiles",str),("bamfiles",str),("fastqsfiles",str),("realignedfiles",str),("fastq1files",str),("fastq2files",str),("fastqo1files",str),("fastqo2files",str),("fastqfiles",str),("fastqcfiles",str),("createindex",str),("overwriteindex",str),("bypassBiobambam",str),("recalibratebamfiles",str),("hcvcffiles",str),("archive_files",str),("delete_files",str),("archive_prefix",str),("gatk_haplotype_out_bam",str),("gatk_db_out",str),("gatk_gvcf_out_vcf",str),("gatk_refined_out_vcf",str),("pedigree_files",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    work_dir=pset(None)
    genome_dir=pset(None)
    inputFiles=pset([])
    cleanbamfiles=pset([])
    genomefile=pset(None)
    fastqfiles=pset([])
    realignedfiles=pset([])
    pairedend=pset(False)
    bamfiles=pset([])
    fastq1files=pset([])
    fastq2files=pset([])
    fastqo1files=pset([])
    fastqo2files=pset([])
    fastqsfiles=pset([])
    fastqcfiles=pset([])
    overwriteindex=pset(False)
    bypassBiobambam=pset(False)
    recalibratebamfiles=pset([])
    hcvcffiles=pset([])
    archive_files=pset([])
    delete_files=pset([])
    archive_prefix=pset(None)
    prepend_date=pset(True)
    gatk_haplotype_out_bam=pset([])
    gatk_db_out=pset(None)
    gatk_gvcf_out_vcf=pset([])
    gatk_refined_out_vcf=pset(None)
    pedigree_files=pset(None)
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
        if hasattr(self,"inputFiles"):
            outputValue=getattr(self,"inputFiles")
        self.send("inputFiles", outputValue)
        outputValue=None
        if hasattr(self,"genomefile"):
            outputValue=getattr(self,"genomefile")
        self.send("genomefile", outputValue)
        outputValue=None
        if hasattr(self,"cleanbamfiles"):
            outputValue=getattr(self,"cleanbamfiles")
        self.send("cleanbamfiles", outputValue)
        outputValue=None
        if hasattr(self,"bamfiles"):
            outputValue=getattr(self,"bamfiles")
        self.send("bamfiles", outputValue)
        outputValue=None
        if hasattr(self,"fastqsfiles"):
            outputValue=getattr(self,"fastqsfiles")
        self.send("fastqsfiles", outputValue)
        outputValue=None
        if hasattr(self,"realignedfiles"):
            outputValue=getattr(self,"realignedfiles")
        self.send("realignedfiles", outputValue)
        outputValue=None
        if hasattr(self,"fastq1files"):
            outputValue=getattr(self,"fastq1files")
        self.send("fastq1files", outputValue)
        outputValue=None
        if hasattr(self,"fastq2files"):
            outputValue=getattr(self,"fastq2files")
        self.send("fastq2files", outputValue)
        outputValue=None
        if hasattr(self,"fastqo1files"):
            outputValue=getattr(self,"fastqo1files")
        self.send("fastqo1files", outputValue)
        outputValue=None
        if hasattr(self,"fastqo2files"):
            outputValue=getattr(self,"fastqo2files")
        self.send("fastqo2files", outputValue)
        outputValue=None
        if hasattr(self,"fastqfiles"):
            outputValue=getattr(self,"fastqfiles")
        self.send("fastqfiles", outputValue)
        outputValue=None
        if hasattr(self,"fastqcfiles"):
            outputValue=getattr(self,"fastqcfiles")
        self.send("fastqcfiles", outputValue)
        outputValue=None
        if hasattr(self,"createindex"):
            outputValue=getattr(self,"createindex")
        self.send("createindex", outputValue)
        outputValue=None
        if hasattr(self,"overwriteindex"):
            outputValue=getattr(self,"overwriteindex")
        self.send("overwriteindex", outputValue)
        outputValue=None
        if hasattr(self,"bypassBiobambam"):
            outputValue=getattr(self,"bypassBiobambam")
        self.send("bypassBiobambam", outputValue)
        outputValue=None
        if hasattr(self,"recalibratebamfiles"):
            outputValue=getattr(self,"recalibratebamfiles")
        self.send("recalibratebamfiles", outputValue)
        outputValue=None
        if hasattr(self,"hcvcffiles"):
            outputValue=getattr(self,"hcvcffiles")
        self.send("hcvcffiles", outputValue)
        outputValue=None
        if hasattr(self,"archive_files"):
            outputValue=getattr(self,"archive_files")
        self.send("archive_files", outputValue)
        outputValue=None
        if hasattr(self,"delete_files"):
            outputValue=getattr(self,"delete_files")
        self.send("delete_files", outputValue)
        outputValue=None
        if hasattr(self,"archive_prefix"):
            outputValue=getattr(self,"archive_prefix")
        self.send("archive_prefix", outputValue)
        outputValue=None
        if hasattr(self,"gatk_haplotype_out_bam"):
            outputValue=getattr(self,"gatk_haplotype_out_bam")
        self.send("gatk_haplotype_out_bam", outputValue)
        outputValue=None
        if hasattr(self,"gatk_db_out"):
            outputValue=getattr(self,"gatk_db_out")
        self.send("gatk_db_out", outputValue)
        outputValue=None
        if hasattr(self,"gatk_gvcf_out_vcf"):
            outputValue=getattr(self,"gatk_gvcf_out_vcf")
        self.send("gatk_gvcf_out_vcf", outputValue)
        outputValue=None
        if hasattr(self,"gatk_refined_out_vcf"):
            outputValue=getattr(self,"gatk_refined_out_vcf")
        self.send("gatk_refined_out_vcf", outputValue)
        outputValue=None
        if hasattr(self,"pedigree_files"):
            outputValue=getattr(self,"pedigree_files")
        self.send("pedigree_files", outputValue)
