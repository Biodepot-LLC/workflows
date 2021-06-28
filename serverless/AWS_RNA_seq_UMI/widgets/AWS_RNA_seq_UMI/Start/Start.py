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

class OWStart(OWBwBWidget):
    name = "Start"
    description = "Enter workflow parameters and start"
    priority = 10
    icon = getIconName(__file__,"start.png")
    want_main_area = False
    docker_image_name = "biodepot/alpine-bash"
    docker_image_tag = "3.11.6__45283ff2"
    outputs = [("credentials_dir",str),("bucket",str),("region",str),("cloud_dir",str),("parent_dir",str),("local_dir",str),("seqs_dir",str),("executables_dir",str),("cloud_executables_dir",str),("references_dir",str),("cloud_references_dir",str),("aligns_dir",str),("cloud_aligns_dir",str),("DEG_configuration_file",str),("topGenesFile",str),("barcodeFile",str),("safDir",str),("function_zip",str),("function_name",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    credentials_dir=pset("/data/credentials.json")
    bucket=pset(None)
    cloud_dir=pset("gcp_test")
    local_dir=pset(None)
    seqs_dir=pset(None)
    executables_dir=pset(None)
    cloud_executables_dir=pset(None)
    references_dir=pset(None)
    cloud_references_dir=pset(None)
    aligns_dir=pset(None)
    cloud_aligns_dir=pset(None)
    region=pset("us-east-1")
    DEG_configuration_file=pset(None)
    topGenesFile=pset(None)
    barcodeFile=pset(None)
    safDir=pset(None)
    function_zip=pset(None)
    parent_dir=pset(None)
    function_name=pset("dtoxsfunction")
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Start")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"credentials_dir"):
            outputValue=getattr(self,"credentials_dir")
        self.send("credentials_dir", outputValue)
        outputValue=None
        if hasattr(self,"bucket"):
            outputValue=getattr(self,"bucket")
        self.send("bucket", outputValue)
        outputValue=None
        if hasattr(self,"region"):
            outputValue=getattr(self,"region")
        self.send("region", outputValue)
        outputValue=None
        if hasattr(self,"cloud_dir"):
            outputValue=getattr(self,"cloud_dir")
        self.send("cloud_dir", outputValue)
        outputValue=None
        if hasattr(self,"parent_dir"):
            outputValue=getattr(self,"parent_dir")
        self.send("parent_dir", outputValue)
        outputValue=None
        if hasattr(self,"local_dir"):
            outputValue=getattr(self,"local_dir")
        self.send("local_dir", outputValue)
        outputValue=None
        if hasattr(self,"seqs_dir"):
            outputValue=getattr(self,"seqs_dir")
        self.send("seqs_dir", outputValue)
        outputValue=None
        if hasattr(self,"executables_dir"):
            outputValue=getattr(self,"executables_dir")
        self.send("executables_dir", outputValue)
        outputValue=None
        if hasattr(self,"cloud_executables_dir"):
            outputValue=getattr(self,"cloud_executables_dir")
        self.send("cloud_executables_dir", outputValue)
        outputValue=None
        if hasattr(self,"references_dir"):
            outputValue=getattr(self,"references_dir")
        self.send("references_dir", outputValue)
        outputValue=None
        if hasattr(self,"cloud_references_dir"):
            outputValue=getattr(self,"cloud_references_dir")
        self.send("cloud_references_dir", outputValue)
        outputValue=None
        if hasattr(self,"aligns_dir"):
            outputValue=getattr(self,"aligns_dir")
        self.send("aligns_dir", outputValue)
        outputValue=None
        if hasattr(self,"cloud_aligns_dir"):
            outputValue=getattr(self,"cloud_aligns_dir")
        self.send("cloud_aligns_dir", outputValue)
        outputValue=None
        if hasattr(self,"DEG_configuration_file"):
            outputValue=getattr(self,"DEG_configuration_file")
        self.send("DEG_configuration_file", outputValue)
        outputValue=None
        if hasattr(self,"topGenesFile"):
            outputValue=getattr(self,"topGenesFile")
        self.send("topGenesFile", outputValue)
        outputValue=None
        if hasattr(self,"barcodeFile"):
            outputValue=getattr(self,"barcodeFile")
        self.send("barcodeFile", outputValue)
        outputValue=None
        if hasattr(self,"safDir"):
            outputValue=getattr(self,"safDir")
        self.send("safDir", outputValue)
        outputValue=None
        if hasattr(self,"function_zip"):
            outputValue=getattr(self,"function_zip")
        self.send("function_zip", outputValue)
        outputValue=None
        if hasattr(self,"function_name"):
            outputValue=getattr(self,"function_name")
        self.send("function_name", outputValue)
