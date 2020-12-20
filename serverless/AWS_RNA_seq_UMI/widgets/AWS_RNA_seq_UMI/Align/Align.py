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
    icon = getIconName(__file__,"lambda_function.png")
    want_main_area = False
    docker_image_name = "biodepot/lambda_umi_align"
    docker_image_tag = "1.16.272__python_3.8.0__alpine-3.10__ad114c71"
    inputs = [("ExecTrigger",str,"handleInputsExecTrigger"),("DataTrigger",str,"handleInputsDataTrigger"),("RefTrigger",str,"handleInputsRefTrigger"),("DeployTrigger",str,"handleInputsDeployTrigger"),("credentials_dir",str,"handleInputscredentials_dir"),("bucket_name",str,"handleInputsbucket_name"),("region",str,"handleInputsregion"),("work_dir",str,"handleInputswork_dir"),("cloud_aligns_dir",str,"handleInputscloud_aligns_dir"),("function_name",str,"handleInputsfunction_name"),("topic_name",str,"handleInputstopic_name")]
    outputs = [("bucket_name",str),("credentials_dir",str),("topic_name",str),("recv_topic",str),("recv_subscription",str),("function_name",str),("work_dir",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    bucket_name=pset("dtoxsbucket")
    credentials_dir=pset("/data/.aws")
    region=pset("us-east-1")
    topic_name=pset("dtoxspubsub")
    recv_topic=pset("dtoxsrecv")
    recv_subscription=pset("dtoxssubscription")
    function_name=pset("dtoxsfunction")
    fastq_suffix=pset("fq")
    work_dir=pset("dtoxsdir")
    cloud_aligns_dir=pset("")
    upload_dir=pset("saf")
    max_workers=pset(16)
    align_timeout=pset(240)
    start_timeout=pset(60)
    finish_timeout=pset(200)
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
    def handleInputscredentials_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("credentials_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsbucket_name(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("bucket_name", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsregion(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("region", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputswork_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("work_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputscloud_aligns_dir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("cloud_aligns_dir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfunction_name(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("function_name", value, args[0][0], test=args[0][3])
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
        if hasattr(self,"credentials_dir"):
            outputValue=getattr(self,"credentials_dir")
        self.send("credentials_dir", outputValue)
        outputValue=None
        if hasattr(self,"topic_name"):
            outputValue=getattr(self,"topic_name")
        self.send("topic_name", outputValue)
        outputValue=None
        if hasattr(self,"recv_topic"):
            outputValue=getattr(self,"recv_topic")
        self.send("recv_topic", outputValue)
        outputValue=None
        if hasattr(self,"recv_subscription"):
            outputValue=getattr(self,"recv_subscription")
        self.send("recv_subscription", outputValue)
        outputValue=None
        if hasattr(self,"function_name"):
            outputValue=getattr(self,"function_name")
        self.send("function_name", outputValue)
        outputValue=None
        if hasattr(self,"work_dir"):
            outputValue=getattr(self,"work_dir")
        self.send("work_dir", outputValue)
