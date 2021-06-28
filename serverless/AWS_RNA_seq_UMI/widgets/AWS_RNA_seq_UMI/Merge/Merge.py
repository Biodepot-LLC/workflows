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

class OWMerge(OWBwBWidget):
    name = "Merge"
    description = "merge split sam files"
    priority = 10
    icon = getIconName(__file__,"umimerge.png")
    want_main_area = False
    docker_image_name = "biodepot/umimerge"
    docker_image_tag = "ubuntu_18.04__3654016e"
    inputs = [("Trigger",str,"handleInputsTrigger"),("inputDir",str,"handleInputsinputDir"),("baseDir",str,"handleInputsbaseDir")]
    outputs = [("outputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    outputDir=pset(None)
    filter=pset(False)
    symfile=pset(None)
    ercc=pset(None)
    barcode=pset(None)
    inputDir=pset(None)
    umicounts=pset(None)
    threads=pset(1)
    binsize=pset(0)
    sampleID=pset("")
    multiwells=pset(False)
    nwells=pset(96)
    baseDir=pset("/")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Merge")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsinputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbaseDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("baseDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
