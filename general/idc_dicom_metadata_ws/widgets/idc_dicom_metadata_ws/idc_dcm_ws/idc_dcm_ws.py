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

class OWidc_dcm_ws(OWBwBWidget):
    name = "idc_dcm_ws"
    description = "idc dicom web server api"
    priority = 1
    icon = getIconName(__file__,"NIH.png")
    want_main_area = False
    docker_image_name = "varikmp/idc_dcm_ws"
    docker_image_tag = "latest"
    inputs = [("InputFile",str,"handleInputsInputFile")]
    outputs = [("OutputDir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    DOWNLOAD_DIR=pset("")
    DATABASE_FILE=pset("")
    URL_LIST=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"idc_dcm_ws")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsInputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("InputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"OutputDir"):
            outputValue=getattr(self,"OutputDir")
        self.send("OutputDir", outputValue)
