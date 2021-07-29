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

class OWvariant_effect_predictor(OWBwBWidget):
    name = "variant_effect_predictor"
    description = "Annotate raw VCF files using Variant Effect Predictor"
    priority = 90
    icon = getIconName(__file__,"VEP.jpg")
    want_main_area = False
    docker_image_name = "biodepot/vep"
    docker_image_tag = "102.0__ubuntu_18.04__12512944"
    inputs = [("inputFile",str,"handleInputsinputFile"),("fasta",str,"handleInputsfasta"),("vepBaseCacheDir",str,"handleInputsvepBaseCacheDir"),("outputFile",str,"handleInputsoutputFile"),("sniper_trigger",str,"handleInputssniper_trigger"),("varscan_trigger",str,"handleInputsvarscan_trigger"),("muse_call_trigger",str,"handleInputsmuse_call_trigger"),("pindel_trigger",str,"handleInputspindel_trigger"),("mutect_trigger",str,"handleInputsmutect_trigger")]
    outputs = [("outputFile",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    vepHelp=pset(False)
    vepVerbose=pset(False)
    vepConfig=pset(None)
    everything=pset(False)
    species=pset(None)
    assembly=pset(None)
    inputFile=pset([])
    inputData=pset(None)
    format=pset(None)
    outputFile=pset([])
    forceOverwrite=pset(False)
    statsFile=pset(None)
    noStats=pset(False)
    statsText=pset(False)
    warningFile=pset(None)
    maxSvSize=pset(False)
    noCheckVariantsOrder=pset(False)
    fork=pset(None)
    vepCache=pset(False)
    vepBaseCacheDir=pset(None)
    vepCacheDir=pset(None)
    pluginDir=pset(None)
    offline=pset(False)
    fasta=pset(None)
    refSeq=pset(False)
    merged=pset(False)
    cacheVersion=pset(False)
    showCacheInfo=pset(False)
    bufferSize=pset(None)
    plugin=pset(None)
    custom=pset(None)
    gff=pset(None)
    gtf=pset(None)
    bam=pset(None)
    useTranscriptRef=pset(False)
    customMultiAllelic=pset(False)
    vcf=pset(False)
    tab=pset(False)
    json=pset(False)
    compressOutput=pset(None)
    fields=pset(None)
    minimal=pset(False)
    variantClass=pset(False)
    sift=pset(None)
    polyphen=pset(None)
    humdiv=pset(False)
    nearest=pset(None)
    distance=pset(None)
    overlaps=pset(False)
    genePhenotype=pset(False)
    regulatory=pset(False)
    cellType=pset(None)
    individual=pset(None)
    phased=pset(False)
    alleleNumber=pset(False)
    showRefAllele=pset(False)
    totalLength=pset(False)
    vepNumbers=pset(False)
    noEscape=pset(False)
    keepCsq=pset(False)
    vcfInfoField=pset(None)
    vepTerms=pset(None)
    noHeaders=pset(False)
    shift3prime=pset(None)
    shiftGenomic=pset(None)
    shiftLength=pset(False)
    ccds=pset(False)
    hgvs=pset(False)
    vepSymbol=pset(False)
    vepDomains=pset(False)
    vepCanonical=pset(False)
    protein=pset(False)
    biotype=pset(False)
    uniprot=pset(False)
    tsl=pset(False)
    shiftHgvs=pset(None)
    checkExisting=pset(False)
    xrefRefseq=pset(False)
    vepFailed=pset(None)
    flagPickAllele=pset(False)
    pickOrder=pset(None)
    pubmed=pset(False)
    af=pset(False)
    af1kg=pset(False)
    afEsp=pset(False)
    afGnomad=pset(False)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"variant_effect_predictor")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsinputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("inputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsfasta(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("fasta", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsvepBaseCacheDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("vepBaseCacheDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsoutputFile(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputFile", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssniper_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sniper_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsvarscan_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("varscan_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmuse_call_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("muse_call_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputspindel_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("pindel_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmutect_trigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("mutect_trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"outputFile"):
            outputValue=getattr(self,"outputFile")
        self.send("outputFile", outputValue)
