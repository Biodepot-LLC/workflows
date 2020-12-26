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
    icon = getIconName(__file__,"bwasamsort.png")
    want_main_area = False
    docker_image_name = "biodepot/bwa-samtools"
    docker_image_tag = "gdcalign__alpine_3.12"
    inputs = [("readgroup",str,"handleInputsreadgroup"),("reference",str,"handleInputsreference"),("trigger",str,"handleInputstrigger")]
    outputs = [("outputFiles",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    readgroup=pset([])
    reference=pset([])
    fastq_files=pset([])
    threads=pset([])
    minscore=pset(None)
    outputfiles=pset([])
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
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFiles"):
            outputValue=getattr(self,"outputFiles")
        self.send("outputFiles", outputValue)
