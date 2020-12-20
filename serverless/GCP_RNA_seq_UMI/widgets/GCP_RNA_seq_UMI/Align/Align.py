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

class OWAlign(OWBwBWidget):
    name = "Align"
    description = "Setup and launch lambda functions"
    priority = 10
    icon = getIconName(__file__,"google_function.png")
    want_main_area = False
    docker_image_name = "biodepot/gcpalign"
    docker_image_tag = "python_3.8.0__alpine_3.10__3eac364c"
    inputs = [("ExecTrigger",str,"handleInputsExecTrigger"),("DataTrigger",str,"handleInputsDataTrigger"),("RefTrigger",str,"handleInputsRefTrigger"),("DeployTrigger",str,"handleInputsDeployTrigger"),("credentials_file",str,"handleInputscredentials_file"),("bucket_name",str,"handleInputsbucket_name"),("project_id",str,"handleInputsproject_id"),("upload_dir",str,"handleInputsupload_dir"),("work_dir",str,"handleInputswork_dir"),("aligns_dir",str,"handleInputsaligns_dir"),("topic_name",str,"handleInputstopic_name")]
    outputs = [("bucket_name",str),("credentials_file",str),("topic_name",str),("recv_topic",str),("work_dir",str),("upload_dir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    bucket_name=pset("gcpdtoxsbucket")
    topic_name=pset("gcpdtoxspubsub")
    work_dir=pset("dtoxsdir")
    aligns_dir=pset("")
    recv_topic=pset("dtoxsrecv")
    fastq_suffix=pset("fq")
    upload_dir=pset("saf")
    project_id=pset("serverless_user_123")
    max_workers=pset(16)
    start_timeout=pset(600)
    align_timeout=pset(1000)
    finish_timeout=pset(900)
    credentials_file=pset("/data/credentials.json")
    bwa_n=pset("0.04")
    bwa_o=pset(1)
    bwa_e=pset(-1)
    bwa_i=pset(5)
    bwa_d=pset(10)
    bwa_l=pset(32)
    bwa_k=pset(2)
    bwa_m=pset(2000000)
    bwa_t=pset(1)
    bwa_M=pset(3)
    bwa_O=pset(11)
    bwa_E=pset(4)
    bwa_R=pset(20)
    bwa_q=pset(0)
    bwa_L=pset(False)
    bwa_N=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"Align")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsExecTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("ExecTrigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsDataTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("DataTrigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsRefTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("RefTrigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsDeployTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("DeployTrigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputscredentials_file(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("credentials_file", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbucket_name(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("bucket_name", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsproject_id(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("project_id", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsupload_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("upload_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputswork_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("work_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsaligns_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("aligns_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputstopic_name(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("topic_name", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"bucket_name"):
            outputValue=getattr(self,"bucket_name")
        self.send("bucket_name", outputValue)
        outputValue=None
        if hasattr(self,"credentials_file"):
            outputValue=getattr(self,"credentials_file")
        self.send("credentials_file", outputValue)
        outputValue=None
        if hasattr(self,"topic_name"):
            outputValue=getattr(self,"topic_name")
        self.send("topic_name", outputValue)
        outputValue=None
        if hasattr(self,"recv_topic"):
            outputValue=getattr(self,"recv_topic")
        self.send("recv_topic", outputValue)
        outputValue=None
        if hasattr(self,"work_dir"):
            outputValue=getattr(self,"work_dir")
        self.send("work_dir", outputValue)
        outputValue=None
        if hasattr(self,"upload_dir"):
            outputValue=getattr(self,"upload_dir")
        self.send("upload_dir", outputValue)
