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

class OWconsolidate(OWBwBWidget):
    name = "consolidate"
    description = "alpine bash with wget curl gzip bzip2"
    priority = 1
    icon = getIconName(__file__,"consolidation.png")
    want_main_area = False
    docker_image_name = "biodepot/bash-utils"
    docker_image_tag = "alpine-3.7__081418"
    inputs = [("InputDir1",str,"handleInputsInputDir1"),("InputDir2",str,"handleInputsInputDir2"),("InputDir3",str,"handleInputsInputDir3"),("InputDir4",str,"handleInputsInputDir4"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    Data=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"consolidate")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsInputDir1(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("InputDir1", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsInputDir2(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("InputDir2", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsInputDir3(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("InputDir3", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsInputDir4(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("InputDir4", value, args[0][0], test=args[0][3])
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
