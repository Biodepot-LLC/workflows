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

class OWhtseq(OWBwBWidget):
    name = "htseq"
    description = "Enter and output a file"
    priority = 10
    icon = getIconName(__file__,"htseq.png")
    want_main_area = False
    docker_image_name = "biodepot/htseq"
    docker_image_tag = "0.12.4__python3.8-slim-buster__2f8c4603"
    inputs = [("gtffile",str,"handleInputsgtffile"),("inputfile",str,"handleInputsinputfile")]
    outputs = [("outputfile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    filetype=pset("bam")
    order=pset("name")
    maxbuffersize=pset(None)
    stranded=pset("yes")
    MNAQUAL=pset(10)
    featuretype=pset("exon")
    maxreadsinbuffer=pset(None)
    outputfile=pset(None)
    idattr=pset("gene_id")
    additionalattr=pset(None)
    mode=pset("union")
    nonunique=pset(None)
    secondaryalignments=pset(None)
    supplementaryalignments=pset(None)
    samouts=pset(False)
    samtype=pset(None)
    delimiter=pset(None)
    append=pset(False)
    nprocesses=pset(None)
    featurequery=pset(None)
    quietmode=pset(False)
    inputfile=pset(None)
    gtffile=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"htseq")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsgtffile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("gtffile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsinputfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputfile"):
            outputValue=getattr(self,"outputfile")
        self.send("outputfile", outputValue)
