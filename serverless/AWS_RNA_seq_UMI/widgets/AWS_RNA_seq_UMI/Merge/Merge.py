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
    docker_image_tag = "ubuntu_20.04__4d4b6b3f"
    inputs = [("Trigger",str,"handleInputsTrigger"),("inputDir",str,"handleInputsinputDir"),("baseDir",str,"handleInputsbaseDir"),("markmultihits",str,"handleInputsmarkmultihits"),("properPairs",str,"handleInputsproperPairs"),("marknonrefseq",str,"handleInputsmarknonrefseq"),("samegenenotmulti",str,"handleInputssamegenenotmulti"),("nbins",str,"handleInputsnbins"),("binsize",str,"handleInputsbinsize")]
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
    sampleID=pset("")
    multiwells=pset(False)
    nwells=pset(96)
    baseDir=pset("/")
    markmultihits=pset(False)
    properPairs=pset(False)
    marknonrefseq=pset(False)
    samegenenotmulti=pset(False)
    nfastqs=pset(None)
    nbins=pset(16)
    binsize=pset(0)
    barcodesize=pset(6)
    umisize=pset(10)
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
    def handleInputsmarkmultihits(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("markmultihits", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsproperPairs(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("properPairs", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmarknonrefseq(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("marknonrefseq", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssamegenenotmulti(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("samegenenotmulti", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsnbins(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("nbins", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbinsize(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("binsize", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
