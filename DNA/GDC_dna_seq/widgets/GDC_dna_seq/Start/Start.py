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
    priority = 1
    icon = getIconName(__file__,"start.png")
    want_main_area = False
    docker_image_name = "biodepot/gdc-mrna-start"
    docker_image_tag = "alpine_3.12__59b7cb77"
    outputs = [("work_dir",str),("genome_dir",str),("inputFiles",str),("genomefile",str),("cleanfiles",str),("gdccredentials",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    work_dir=pset(None)
    genome_dir=pset(None)
    inputFiles=pset([])
    cleanfiles=pset([])
    genomefile=pset(None)
    gdccredentials=pset(None)
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
        if hasattr(self,"work_dir"):
            outputValue=getattr(self,"work_dir")
        self.send("work_dir", outputValue)
        outputValue=None
        if hasattr(self,"genome_dir"):
            outputValue=getattr(self,"genome_dir")
        self.send("genome_dir", outputValue)
        outputValue=None
        if hasattr(self,"inputFiles"):
            outputValue=getattr(self,"inputFiles")
        self.send("inputFiles", outputValue)
        outputValue=None
        if hasattr(self,"genomefile"):
            outputValue=getattr(self,"genomefile")
        self.send("genomefile", outputValue)
        outputValue=None
        if hasattr(self,"cleanfiles"):
            outputValue=getattr(self,"cleanfiles")
        self.send("cleanfiles", outputValue)
        outputValue=None
        if hasattr(self,"gdccredentials"):
            outputValue=getattr(self,"gdccredentials")
        self.send("gdccredentials", outputValue)
