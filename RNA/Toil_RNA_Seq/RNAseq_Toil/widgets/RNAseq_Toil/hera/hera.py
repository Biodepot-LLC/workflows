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

class OWhera(OWBwBWidget):
    name = "hera"
    description = "Hera 1.1"
    priority = 1
    icon = getIconName(__file__,"bioturing.png")
    want_main_area = False
    docker_image_name = "quay.io/ucsc_cgl/hera"
    docker_image_tag = "1.1--5f2b2b45776536d46a60b377b52b846694c534bd"
    inputs = [("FastQPairedTrimmedFiles",str,"handleInputsFastQPairedTrimmedFiles"),("HeraIndexFile",str,"handleInputsHeraIndexFile"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    Method=pset(None)
    IndexDir=pset(None)
    FastQFile1=pset(None)
    FastQFile2=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"hera")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsFastQPairedTrimmedFiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("FastQPairedTrimmedFiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsHeraIndexFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("HeraIndexFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
