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

class OWbwa_index(OWBwBWidget):
    name = "bwa_index"
    description = "Aligns paired-end sequences, sort and return bam files"
    priority = 30
    icon = getIconName(__file__,"bwasamsort.png")
    want_main_area = False
    docker_image_name = "biodepot/bwa-samtools-gdc"
    docker_image_tag = "0.7.15__1.9.52__alpine_3.12"
    inputs = [("reference",str,"handleInputsreference"),("overwrite",str,"handleInputsoverwrite"),("reference_trigger",str,"handleInputsreference_trigger")]
    outputs = [("reference",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    reference=pset(None)
    threads=pset(None)
    prefix=pset(None)
    blocksize=pset(10000000)
    algorithm=pset("rb2")
    overwrite=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"bwa_index")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoverwrite(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("overwrite", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"reference"):
            outputValue=getattr(self,"reference")
        self.send("reference", outputValue)
