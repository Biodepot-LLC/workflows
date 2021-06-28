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

class OWCreate_gbucket(OWBwBWidget):
    name = "Create_gbucket"
    description = "Enter and output a file"
    priority = 10
    icon = getIconName(__file__,"google_add.png")
    want_main_area = False
    docker_image_name = "biodepot/gcpcreate"
    docker_image_tag = "python_3.8.0__alpine_3.10__d4f38112"
    inputs = [("Trigger",str,"handleInputsTrigger"),("credentials_file",str,"handleInputscredentials_file"),("bucket",str,"handleInputsbucket")]
    outputs = [("credentials_file",str),("bucket",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    credentials_file=pset("/data/credentials.json")
    bucket=pset("myBucket")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Create_gbucket")) as f:
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
    def handleInputscredentials_file(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("credentials_file", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbucket(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("bucket", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"credentials_file"):
            outputValue=getattr(self,"credentials_file")
        self.send("credentials_file", outputValue)
        outputValue=None
        if hasattr(self,"bucket"):
            outputValue=getattr(self,"bucket")
        self.send("bucket", outputValue)
