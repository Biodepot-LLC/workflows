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

class OWgcpdeploy(OWBwBWidget):
    name = "gcpdeploy"
    description = "Deploy a function to google cloud"
    priority = 10
    icon = getIconName(__file__,"google_function_deploy.png")
    want_main_area = False
    docker_image_name = "biodepot/gcpdeploy"
    docker_image_tag = "277.0.0-alpine__17f895c7"
    inputs = [("Trigger",str,"handleInputsTrigger"),("credentials_file",str,"handleInputscredentials_file"),("bucket",str,"handleInputsbucket"),("function_dir",str,"handleInputsfunction_dir"),("function_name",str,"handleInputsfunction_name"),("region",str,"handleInputsregion"),("topic_id",str,"handleInputstopic_id")]
    outputs = [("function_name",str),("topic_id",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    credentials_file=pset("/data/credentials.json")
    bucket=pset(None)
    function_name=pset(None)
    function_dir=pset(None)
    entrypoint=pset("gcp_handler")
    runtime=pset("python37")
    topic_id=pset(None)
    timeout=pset(300)
    memory=pset(256)
    maxInstances=pset(1000)
    region=pset("us-central1")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"gcpdeploy")) as f:
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
    def handleInputsfunction_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("function_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfunction_name(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("function_name", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsregion(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("region", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstopic_id(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("topic_id", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"function_name"):
            outputValue=getattr(self,"function_name")
        self.send("function_name", outputValue)
        outputValue=None
        if hasattr(self,"topic_id"):
            outputValue=getattr(self,"topic_id")
        self.send("topic_id", outputValue)
