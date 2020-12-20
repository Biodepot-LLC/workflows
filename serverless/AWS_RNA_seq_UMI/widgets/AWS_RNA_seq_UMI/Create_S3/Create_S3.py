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

class OWCreate_S3(OWBwBWidget):
    name = "Create_S3"
    description = "Enter and output a file"
    priority = 10
    icon = getIconName(__file__,"addS3.png")
    want_main_area = False
    docker_image_name = "biodepot/awss3create"
    docker_image_tag = "1.16.272__python_3.8.0__alpine-3.10__d4f38112"
    inputs = [("Trigger",str,"handleInputsTrigger"),("credentials_dir",str,"handleInputscredentials_dir"),("bucket",str,"handleInputsbucket"),("region",str,"handleInputsregion")]
    outputs = [("credentials_dir",str),("bucket",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    credentials_dir=pset("/data/.aws")
    bucket=pset("myBucket")
    region=pset("us-east-1")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Create_S3")) as f:
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
    def handleInputscredentials_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("credentials_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbucket(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("bucket", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsregion(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("region", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"credentials_dir"):
            outputValue=getattr(self,"credentials_dir")
        self.send("credentials_dir", outputValue)
        outputValue=None
        if hasattr(self,"bucket"):
            outputValue=getattr(self,"bucket")
        self.send("bucket", outputValue)
