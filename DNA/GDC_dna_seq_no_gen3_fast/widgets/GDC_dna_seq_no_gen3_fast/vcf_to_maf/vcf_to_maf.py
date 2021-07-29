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

class OWvcf_to_maf(OWBwBWidget):
    name = "vcf_to_maf"
    description = "Convert a VCF into a MAF"
    priority = 100
    icon = getIconName(__file__,"vcf_to_maf.png")
    want_main_area = False
    docker_image_name = "biodepot/vcf_to_maf"
    docker_image_tag = "1.6.19__fbd89e9f"
    inputs = [("inputFile",str,"handleInputsinputFile"),("refFasta",str,"handleInputsrefFasta"),("trigger",str,"handleInputstrigger"),("outputFile",str,"handleInputsoutputFile")]
    outputs = [("outputFile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    inputFile=pset([])
    outputFile=pset([])
    inhibitVep=pset(False)
    refFasta=pset(None)
    tmpDir=pset(None)
    tumorId=pset(None)
    normalId=pset(None)
    vcfTumorId=pset(None)
    vcfNormalId=pset(None)
    customEnst=pset([])
    vepPath=pset("/usr/local/bin")
    vepData=pset("/data/vep")
    vepForks=pset(None)
    bufferSize=pset(None)
    anyAllele=pset(False)
    online=pset(False)
    filterVcf=pset(None)
    maxFilterAc=pset(None)
    species=pset(None)
    ncbiBuild=pset(None)
    cacheVersion=pset(None)
    mafCenter=pset(None)
    retainInfo=pset(None)
    retainFmt=pset(None)
    minHomVaf=pset(None)
    remapChain=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"vcf_to_maf")) as f:
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
    def handleInputsrefFasta(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("refFasta", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFile"):
            outputValue=getattr(self,"outputFile")
        self.send("outputFile", outputValue)
