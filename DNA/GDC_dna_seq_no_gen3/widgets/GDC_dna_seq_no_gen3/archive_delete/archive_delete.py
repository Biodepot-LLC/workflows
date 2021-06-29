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

class OWarchive_delete(OWBwBWidget):
    name = "archive_delete"
    description = "Archive and/or delete selected files"
    priority = 1
    icon = getIconName(__file__,"archive-delete.png")
    want_main_area = False
    docker_image_name = "biodepot/gdc-dna-seq-cleanup"
    docker_image_tag = "alpine_1.13.5__4701c5b2"
    inputs = [("trigger",str,"handleInputstrigger"),("archive_files",str,"handleInputsarchive_files"),("archive_prefix",str,"handleInputsarchive_prefix"),("archive_location",str,"handleInputsarchive_location"),("archive_compression_type",str,"handleInputsarchive_compression_type"),("archive_change_to_dir",str,"handleInputsarchive_change_to_dir"),("delete_files",str,"handleInputsdelete_files")]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    archive_files=pset([])
    archive_prefix=pset(None)
    archive_location=pset(None)
    archive_compression_type=pset(None)
    archive_change_to_dir=pset(None)
    delete_files=pset([])
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"archive_delete")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputstrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsarchive_files(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("archive_files", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsarchive_prefix(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("archive_prefix", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsarchive_location(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("archive_location", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsarchive_compression_type(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("archive_compression_type", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsarchive_change_to_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("archive_change_to_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsdelete_files(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("delete_files", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
