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

class OWgatk_genotypeGVCFs(OWBwBWidget):
    name = "gatk_genotypeGVCFs"
    description = "Base quality recalibration using GATK"
    priority = 40
    icon = getIconName(__file__,"gatk-genotype-gvcf.png")
    want_main_area = False
    docker_image_name = "biodepot/gatk"
    docker_image_tag = "test"
    inputs = [("inputfile",str,"handleInputsinputfile"),("reference",str,"handleInputsreference"),("reference_trigger",str,"handleInputsreference_trigger"),("output",str,"handleInputsoutput")]
    outputs = [("output",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    reference=pset(None)
    inputfile=pset(None)
    output=pset([])
    alleles=pset([])
    annotateNum=pset(False)
    annotation=pset([])
    annotationgroup=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"gatk_genotypeGVCFs")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputfile", value, args[0][0], test=args[0][3])
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
