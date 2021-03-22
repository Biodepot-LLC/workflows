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
    docker_image_tag = "test"
    outputs = [("work_dir",str),("genome_dir",str),("inputFiles",str),("genomefile",str),("cleanfiles",str),("gdccredentials",str),("gdctoken",str),("vepDirectory",str),("bamfiles",str),("fastqsfiles",str),("realignedfiles",str),("fastq1files",str),("fastq2files",str),("fastqo1files",str),("fastqo2files",str),("fastqfiles",str),("createindex",str),("overwriteindex",str),("bypasBiobambam",str)]
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
    cleanfiles=pset([])
    genomefile=pset(None)
    gdccredentials=pset(None)
    gdctoken=pset(None)
    vepDirectory=pset(None)
    fastqfiles=pset([])
    realignedfiles=pset([])
    pairedend=pset(False)
    bamfiles=pset([])
    fastq1files=pset([])
    fastq2files=pset([])
    fastqo1files=pset([])
    fastqo2files=pset([])
    fastqsfiles=pset([])
    overwriteindex=pset(False)
    bypassBiobambam=pset(False)
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
        if hasattr(self,"cleanfiles"):
            outputValue=getattr(self,"cleanfiles")
        self.send("cleanfiles", outputValue)
        outputValue=None
        if hasattr(self,"gdccredentials"):
            outputValue=getattr(self,"gdccredentials")
        self.send("gdccredentials", outputValue)
        outputValue=None
        if hasattr(self,"gdctoken"):
            outputValue=getattr(self,"gdctoken")
        self.send("gdctoken", outputValue)
        outputValue=None
        if hasattr(self,"vepDirectory"):
            outputValue=getattr(self,"vepDirectory")
        self.send("vepDirectory", outputValue)
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
        if hasattr(self,"createindex"):
            outputValue=getattr(self,"createindex")
        self.send("createindex", outputValue)
        outputValue=None
        if hasattr(self,"overwriteindex"):
            outputValue=getattr(self,"overwriteindex")
        self.send("overwriteindex", outputValue)
        outputValue=None
        if hasattr(self,"bypasBiobambam"):
            outputValue=getattr(self,"bypasBiobambam")
        self.send("bypasBiobambam", outputValue)
