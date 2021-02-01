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

class OWvariant_effect_predictor(OWBwBWidget):
    name = "variant_effect_predictor"
    description = "Annotate raw VCF files using Variant Effect Predictor"
    priority = 90
    icon = getIconName(__file__,"VEP.jpg")
    want_main_area = False
    docker_image_name = "ensemblorg/ensembl-vep"
    docker_image_tag = "release_102.0"
    inputs = [("inputFile",str,"handleInputsinputFile")]
    outputs = [("outputFile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    vepHelp=pset(False)
    vepVerbose=pset(False)
    vepConfig=pset(None)
    vepEverything=pset(False)
    species=pset(None)
    vepAssembly=pset(None)
    inputFile=pset(None)
    inputData=pset(None)
    vepFormat=pset(None)
    outputFile=pset(None)
    forceOverwrite=pset(False)
    vepStatsFile=pset(None)
    vepNoStats=pset(False)
    vepStatsText=pset(False)
    vepWarningFile=pset(None)
    maxSvSize=pset(False)
    noCheckVariantsOrder=pset(False)
    vepFork=pset(None)
    vepCache=pset(False)
    vepBaseCacheDir=pset(None)
    vepCacheDir=pset(None)
    vepPluginDir=pset(None)
    vepOffline=pset(False)
    fasta=pset(None)
    vepRefSeq=pset(False)
    vepMerged=pset(False)
    vepCacheVersion=pset(False)
    vepShowCacheInfo=pset(False)
    vepBufferSize=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"variant_effect_predictor")) as f:
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
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFile"):
            outputValue=getattr(self,"outputFile")
        self.send("outputFile", outputValue)
