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

class OWbaserecalibrate(OWBwBWidget):
    name = "baserecalibrate"
    description = "Enter and output a file"
    priority = 10
    icon = getIconName(__file__,"gatk-bsqr.png")
    want_main_area = False
    docker_image_name = "biodepot/gatk3-co-clean"
    docker_image_tag = "3.7__4b439637"
    inputs = [("inputfiles",str,"handleInputsinputfiles"),("reference",str,"handleInputsreference"),("reference_trigger",str,"handleInputsreference_trigger"),("snps_trigger",str,"handleInputssnps_trigger")]
    outputs = [("outputfiles",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    reference=pset(None)
    known=pset(None)
    inputfiles=pset([])
    output=pset([])
    nct=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"baserecalibrate")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputfiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputfiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreference_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssnps_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("snps_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputfiles"):
            outputValue=getattr(self,"outputfiles")
        self.send("outputfiles", outputValue)
