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

class OWstarIndex(OWBwBWidget):
    name = "starIndex"
    description = "Construct indices for STAR aligner "
    priority = 11
    icon = getIconName(__file__,"starIndex.png")
    want_main_area = False
    docker_image_name = "biodepot/star"
    docker_image_tag = "2.4.0e-2.7.9a__debian-8.11-slim__36b899a1"
    inputs = [("Trigger",str,"handleInputsTrigger"),("genomeDir",str,"handleInputsgenomeDir"),("sjdbGTFfile",str,"handleInputssjdbGTFfile"),("genomeFastaFiles",str,"handleInputsgenomeFastaFiles"),("bypass",str,"handleInputsbypass"),("starVersion",str,"handleInputsstarVersion")]
    outputs = [("genomeDir",str),("starVersion",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    rmode=pset("genomeGenerate")
    genomeDir=pset(None)
    genomeFastaFiles=pset(None)
    genomeChrBinNbits=pset("18")
    genomeSAindexNbases=pset(14)
    genomeSAsparseD=pset(1)
    genomeSuffixLengthMax=pset(-1)
    runThreadN=pset(1)
    sjdbGTFfile=pset(None)
    sjdbFileChrStartEnd =pset([])
    sjdbGTFchrPrefix =pset("chr")
    sjdbGTFfeatureExon=pset("exon")
    sjdbGTFtagExonParentTranscript=pset("transcript_id")
    sjdbGTFtagExonParentGene=pset("gene_id")
    sjdbOverhang=pset(100)
    sjdbScore=pset(2)
    sjdbInsertSave =pset("Basic")
    bypass=pset(True)
    starversion=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"starIndex")) as f:
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
    def handleInputsgenomeDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("genomeDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssjdbGTFfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sjdbGTFfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsgenomeFastaFiles(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("genomeFastaFiles", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbypass(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("bypass", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsstarVersion(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("starVersion", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"genomeDir"):
            outputValue=getattr(self,"genomeDir")
        self.send("genomeDir", outputValue)
        outputValue=None
        if hasattr(self,"starVersion"):
            outputValue=getattr(self,"starVersion")
        self.send("starVersion", outputValue)
