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

class OWGDC_mRNA_multi_dr32_fpkm_fpkm(OWBwBWidget):
    name = "GDC_mRNA_multi_dr32_fpkm_fpkm"
    description = "Calculates fpkm and fpkm-UC using gdc formula"
    priority = 10
    icon = getIconName(__file__,"normalize_pl.png")
    want_main_area = False
    docker_image_name = "biodepot/fpkm"
    docker_image_tag = "latest"
    inputs = [("geneinfofile",str,"handleInputsgeneinfofile"),("countsfile",str,"handleInputscountsfile"),("countsfilecreated",str,"handleInputscountsfilecreated")]
    outputs = [("countsfile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    geneinfofile=pset("/data/gencode.gene.info.v22.tsv")
    countsfile=pset(None)
    starformat=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"GDC_mRNA_multi_dr32_fpkm_fpkm")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsgeneinfofile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("geneinfofile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputscountsfile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("countsfile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputscountsfilecreated(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("countsfilecreated", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"countsfile"):
            outputValue=getattr(self,"countsfile")
        self.send("countsfile", outputValue)
