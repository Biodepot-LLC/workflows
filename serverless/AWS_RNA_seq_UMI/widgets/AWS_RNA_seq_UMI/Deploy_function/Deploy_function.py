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

class OWDeploy_function(OWBwBWidget):
    name = "Deploy_function"
    description = "Setup and launch lambda functions"
    priority = 10
    icon = getIconName(__file__,"lambda_function.png")
    want_main_area = False
    docker_image_name = "biodepot/deploy_lambda"
    docker_image_tag = "1.16.272__python_3.8.0__alpine-3.10__490a5b29"
    inputs = [("credentials_dir",str,"handleInputscredentials_dir"),("function_zip",str,"handleInputsfunction_zip"),("function_name",str,"handleInputsfunction_name"),("function_region",str,"handleInputsfunction_region"),("Trigger",str,"handleInputsTrigger")]
    outputs = [("bucket_name",str),("credentials_dir",str),("topic_name",str),("function_name",str),("policy_name",str),("role_name",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    credentials_dir=pset("/data/.aws")
    topic_name=pset("dtoxspubsub")
    function_name=pset("dtoxsfunction")
    function_region=pset("us-east-1")
    handler=pset("main.lambda_handler")
    memory=pset(2048)
    timeout=pset(540)
    policy_name=pset("dtoxspolicy")
    role_name=pset("dtoxsrole")
    function_zip=pset("/data/dtoxsfunction.zip")
    user_id=pset("dtoxsuser")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Deploy_function")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputscredentials_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("credentials_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfunction_zip(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("function_zip", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfunction_name(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("function_name", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfunction_region(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("function_region", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"bucket_name"):
            outputValue=getattr(self,"bucket_name")
        self.send("bucket_name", outputValue)
        outputValue=None
        if hasattr(self,"credentials_dir"):
            outputValue=getattr(self,"credentials_dir")
        self.send("credentials_dir", outputValue)
        outputValue=None
        if hasattr(self,"topic_name"):
            outputValue=getattr(self,"topic_name")
        self.send("topic_name", outputValue)
        outputValue=None
        if hasattr(self,"function_name"):
            outputValue=getattr(self,"function_name")
        self.send("function_name", outputValue)
        outputValue=None
        if hasattr(self,"policy_name"):
            outputValue=getattr(self,"policy_name")
        self.send("policy_name", outputValue)
        outputValue=None
        if hasattr(self,"role_name"):
            outputValue=getattr(self,"role_name")
        self.send("role_name", outputValue)
