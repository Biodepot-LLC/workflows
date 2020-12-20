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

class OWbwa_mem(OWBwBWidget):
    name = "bwa_mem"
    description = "Aligns paired-end sequences"
    priority = 20
    icon = getIconName(__file__,"bwa-mem.png")
    want_main_area = False
    docker_image_name = "biodepot/alpine-bwa-samtools"
    docker_image_tag = "3.7-0.7.15-1.9-52-g651bf14"
    inputs = [("readgroup",str,"handleInputsreadgroup"),("reference",str,"handleInputsreference"),("fastq_1",str,"handleInputsfastq_1"),("fastq_2",str,"handleInputsfastq_2"),("trigger",str,"handleInputstrigger")]
    outputs = [("outputFile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    outputFile=pset("/data/output-bwa.sam")
    readgroup=pset(None)
    reference=pset("/data/GRCh38.d1.vd1.fa")
    fastq_1=pset("/data/*_1.fq.gz")
    fastq_2=pset("/data/*_2.fq.gz")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"bwa_mem")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsreadgroup(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("readgroup", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfastq_1(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("fastq_1", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfastq_2(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("fastq_2", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFile"):
            outputValue=getattr(self,"outputFile")
        self.send("outputFile", outputValue)
