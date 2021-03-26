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

class OWcutadapt(OWBwBWidget):
    name = "cutadapt"
    description = "Cut Adapter"
    priority = 1
    icon = getIconName(__file__,"cutadapt.png")
    want_main_area = False
    docker_image_name = "varikmp/cutadapt"
    docker_image_tag = "latest"
    inputs = [("FastQPairedFiles",str,"handleInputsFastQPairedFiles"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("FastQPairedTrimmedFiles",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    ADAPTER_1=pset(None)
    LENGTH=pset(None)
    ADAPTER_2=pset(None)
    OUTPUT_1=pset(None)
    OUTPUT_2=pset(None)
    INPUT_1=pset(None)
    INPUT_2=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"cutadapt")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsFastQPairedFiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("FastQPairedFiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"FastQPairedTrimmedFiles"):
            outputValue=getattr(self,"FastQPairedTrimmedFiles")
        self.send("FastQPairedTrimmedFiles", outputValue)
