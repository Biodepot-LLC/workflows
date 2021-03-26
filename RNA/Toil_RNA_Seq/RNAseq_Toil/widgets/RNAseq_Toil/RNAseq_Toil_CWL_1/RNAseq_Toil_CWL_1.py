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

class OWRNAseq_Toil_CWL_1(OWBwBWidget):
    name = "RNAseq_Toil_CWL_1"
    description = "Toil CWL"
    priority = 1
    icon = getIconName(__file__,"cwl.png")
    want_main_area = False
    docker_image_name = "varikmp/toil_docker"
    docker_image_tag = "latest"
    inputs = [("trimmedFastQFile",str,"handleInputstrimmedFastQFile"),("indexFile",str,"handleInputsindexFile"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    CWL_FILE=pset(None)
    YAML_FILE=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"RNAseq_Toil_CWL_1")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputstrimmedFastQFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trimmedFastQFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsindexFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("indexFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
