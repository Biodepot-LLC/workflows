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

class OWgatk_HC(OWBwBWidget):
    name = "gatk_HC"
    description = "Base quality recalibration using GATK"
    priority = 40
    icon = getIconName(__file__,"gatk-hc.png")
    want_main_area = False
    docker_image_name = "biodepot/gatk"
    docker_image_tag = "test"
    inputs = [("inputfiles",str,"handleInputsinputfiles"),("reference",str,"handleInputsreference"),("reference_trigger",str,"handleInputsreference_trigger"),("snps_trigger",str,"handleInputssnps_trigger"),("output",str,"handleInputsoutput")]
    outputs = [("output",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    reference=pset(None)
    inputfiles=pset([])
    output=pset([])
    alleles=pset([])
    annotateNum=pset(False)
    annotation=pset([])
    annotationgroup=pset([])
    emitrefconf=pset(None)
    bamout=pset([])
    regions=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"gatk_HC")) as f:
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
    def handleInputsoutput(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("output", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"output"):
            outputValue=getattr(self,"output")
        self.send("output", outputValue)
