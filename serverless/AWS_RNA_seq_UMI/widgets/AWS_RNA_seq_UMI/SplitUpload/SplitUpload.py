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

class OWSplitUpload(OWBwBWidget):
    name = "SplitUpload"
    description = "Splits and demuxes fastq files"
    priority = 10
    icon = getIconName(__file__,"umisplit.png")
    want_main_area = False
    docker_image_name = "biodepot/umisplit_awsupload"
    docker_image_tag = "1.16.272__python_3.8.0__alpine-3.10__7130cd7b"
    inputs = [("Trigger",str,"handleInputsTrigger"),("credentials_dir",str,"handleInputscredentials_dir"),("seqs_dir",str,"handleInputsseqs_dir"),("bucket",str,"handleInputsbucket"),("cloud_dir",str,"handleInputscloud_dir"),("outputdir",str,"handleInputsoutputdir"),("barcode",str,"handleInputsbarcode")]
    outputs = [("outputdir",str),("cloud_dir",str),("bucket",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    credentials_dir=pset("/data/.aws")
    cloud_dir=pset(None)
    bucket=pset(None)
    split_threads=pset(1)
    seqs_dir=pset(None)
    barcode=pset(None)
    outputdir=pset("/data")
    filter=pset(False)
    compress=pset(False)
    maxsize=pset(100000)
    length=pset(16)
    minqual=pset(10)
    maxmismatch=pset(0)
    nwells=pset(96)
    upload_threads=pset(2)
    upload_threads_after=pset(4)
    done_file=pset(False)
    nfiles=pset(12)
    npairs=pset(6)
    fastq_suffix=pset("fastq.gz")
    R1fastq_suffix=pset("R1.fastq.gz")
    R2fastq_suffix=pset("R2.fastq.gz")
    maxambig=pset(0)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"SplitUpload")) as f:
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
    def handleInputsseqs_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("seqs_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbucket(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("bucket", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputscloud_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("cloud_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputdir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputdir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbarcode(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("barcode", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputdir"):
            outputValue=getattr(self,"outputdir")
        self.send("outputdir", outputValue)
        outputValue=None
        if hasattr(self,"cloud_dir"):
            outputValue=getattr(self,"cloud_dir")
        self.send("cloud_dir", outputValue)
        outputValue=None
        if hasattr(self,"bucket"):
            outputValue=getattr(self,"bucket")
        self.send("bucket", outputValue)
