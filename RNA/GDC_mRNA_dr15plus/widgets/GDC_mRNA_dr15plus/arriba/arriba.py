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

class OWarriba(OWBwBWidget):
    name = "arriba"
    description = "Enter and output a file"
    priority = 10
    icon = getIconName(__file__,"arriba.png")
    want_main_area = False
    docker_image_name = "biodepot/arriba"
    docker_image_tag = "v1.1.0__ubuntu_18.04"
    inputs = [("Trigger",str,"handleInputsTrigger"),("annotationfile",str,"handleInputsannotationfile"),("assembly",str,"handleInputsassembly")]
    outputs = [("File",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    chimericinput=pset(None)
    alignmentinput=pset(None)
    assembly=pset(None)
    annotationfile=pset(None)
    blacklist=pset(None)
    knownlist=pset(None)
    structuralvars=pset(None)
    tags=pset(None)
    proteindomains=pset(None)
    outputfile=pset(None)
    discardedfile=pset(None)
    maxdistance=pset(100000)
    strandedness=pset("auto")
    contigs=pset(None)
    vcontigs=pset(None)
    filters=pset(None)
    evalue=pset(0.3)
    minreads=pset(2)
    maxmismaps=pset(0.8)
    maxhomolog=pset(0.3)
    homopolylength=pset(6)
    readthru=pset(10000)
    anchor=pset(None)
    manyspliced=pset(4)
    kmer=pset(0.6)
    mismatch=pset(0.01)
    fragment=pset(200)
    maxreads=pset(300)
    quantile=pset(0.998)
    exonic=pset(0.2)
    topn=pset(5)
    coverage=pset(0.15)
    umis=pset(False)
    extras=pset(False)
    fillgaps=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"arriba")) as f:
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
    def handleInputsannotationfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("annotationfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsassembly(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("assembly", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"File"):
            outputValue=getattr(self,"File")
        self.send("File", outputValue)
