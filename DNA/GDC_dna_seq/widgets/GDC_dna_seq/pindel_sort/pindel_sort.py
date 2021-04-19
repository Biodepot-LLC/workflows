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

class OWpindel_sort(OWBwBWidget):
    name = "pindel_sort"
    description = "Sorts and filters vcf using picard and GATK"
    priority = 76
    icon = getIconName(__file__,"pindel.png")
    want_main_area = False
    docker_image_name = "biodepot/pindel-filter"
    docker_image_tag = "3.6__dbc607bd"
    inputs = [("inputfile",str,"handleInputsinputfile"),("reference_trigger",str,"handleInputsreference_trigger"),("inputfileTrigger",str,"handleInputsinputfileTrigger"),("referencefa",str,"handleInputsreferencefa"),("referencedict",str,"handleInputsreferencedict"),("outputfile",str,"handleInputsoutputfile"),("outputfilterfile",str,"handleInputsoutputfilterfile")]
    outputs = [("outputfile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    referencedict=pset(None)
    referencefa=pset(None)
    inputfile=pset([])
    outputfile=pset([])
    outputfilterfile=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"pindel_sort")) as f:
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
    def handleInputsreference_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("reference_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsinputfileTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputfileTrigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreferencefa(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("referencefa", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreferencedict(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("referencedict", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputfilterfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputfilterfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputfile"):
            outputValue=getattr(self,"outputfile")
        self.send("outputfile", outputValue)
