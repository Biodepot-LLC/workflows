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

class OWBaseRecalibrator(OWBwBWidget):
    name = "BaseRecalibrator"
    description = "Base Recalibrator"
    priority = 20
    icon = getIconName(__file__,"baserecalibrator.png")
    want_main_area = False
    docker_image_name = "biodepot/gatk"
    docker_image_tag = "4.1.9.0__openjdk_8-jre-alpine__cb1b2f17"
    inputs = [("inputFile",str,"handleInputsinputFile"),("reference",str,"handleInputsreference"),("knownSites",str,"handleInputsknownSites"),("trigger",str,"handleInputstrigger")]
    outputs = [("outputGrp",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputFile=pset(None)
    reference=pset(None)
    knownSites=pset([])
    outputGrp=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"BaseRecalibrator")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsknownSites(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("knownSites", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputGrp"):
            outputValue=getattr(self,"outputGrp")
        self.send("outputGrp", outputValue)
