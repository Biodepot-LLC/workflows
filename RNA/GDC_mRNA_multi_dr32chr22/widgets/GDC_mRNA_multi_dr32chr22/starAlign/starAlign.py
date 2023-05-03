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

class OWstarAlign(OWBwBWidget):
    name = "starAlign"
    description = "Star aligner alignment module"
    priority = 12
    icon = getIconName(__file__,"staralign.png")
    want_main_area = False
    docker_image_name = "biodepot/star"
    docker_image_tag = "2.4.0e-2.7.10a__debian-8.11-slim__eb8eacf9"
    inputs = [("trigger",str,"handleInputstrigger"),("outputDir",str,"handleInputsoutputDir"),("genomeDir",str,"handleInputsgenomeDir"),("readFilesIn",str,"handleInputsreadFilesIn"),("sampleTrigger",str,"handleInputssampleTrigger"),("starVersion",str,"handleInputsstarVersion")]
    outputs = [("outputDir",str),("genomeDir",str),("starVersion",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    genomeDir=pset("/data/GenomeDir")
    outputDir=pset("")
    readFilesIn=pset([])
    alignEndsType=pset("Local")
    alignEndsProtrude=pset("0 ConcordantPair")
    alignIntronMax=pset(0)
    alignIntronMin=pset(21)
    alignMatesGapMax=pset(0)
    alignSJDBoverhangMin=pset(3)
    alignSJoverhangMin=pset(5)
    alignSJstitchMismatchNmax=pset(None)
    alignSoftClipAtReferenceEnds=pset("Yes")
    alignSplicedMateMapLmin=pset(0)
    alignSplicedMateMapLminOverLmate=pset(0.66)
    alignWindowsPerReadNmax=pset(10000)
    alignTranscriptsPerReadNmax=pset(10000)
    alignTranscriptsPerWindowNmax=pset(100)
    apelist=pset(False)
    bamRemoveDuplicatesMate2basesN=pset(0)
    bamRemoveDuplicatesType=pset(None)
    chimFilter=pset("banGenomicN")
    chimJunctionOverhangMin=pset(20)
    chimMainSegmentMultNmax=pset(10)
    chimOutType=pset("SeparateSAMold")
    chimScoreDropMax=pset(20)
    chimScoreJunctionNonGTAG=pset(-1)
    chimScoreMin=pset(0)
    chimScoreSeparation=pset(10)
    chimSegmentMin=pset(0)
    chimSegmentReadGapMax=pset(0)
    clip3pAdapterMMp=pset("0.1")
    clip3pAdapterSeq=pset("0")
    clip3pNbases=pset("0")
    clip3pAfterAdapterNbases=pset("0")
    clip5pNbases=pset(None)
    genomeLoad=pset("NoSharedMemory")
    limitIObufferSize=pset(150000000)
    limitOutSAMoneReadBytes=pset(100000)
    limitSjdbInsertNsj=pset(1000000)
    outBAMsortingThreadN=pset(0)
    outBAMcompression=pset(1)
    outFileNamePrefix=pset(None)
    outFilterIntronMotifs=pset(None)
    outFilterMatchNminOverLread=pset(0.66)
    outFilterMismatchNmax=pset(10)
    outFilterMismatchNoverLmax =pset(0.3)
    outFilterMismatchNoverReadLmax=pset(1.0)
    outFilterMultimapNmax=pset(10)
    outFilterMultimapScoreRange=pset(1)
    outFilterScoreMin=pset(0)
    outFilterMatchNmin=pset(0)
    outFilterScoreMinOverLread=pset(0.66)
    outFilterType=pset("Normal")
    outMultimapperOrder=pset("Old_2.4")
    outputFilePrefix=pset(None)
    outReadsUnmapped=pset("")
    outSAMmapqUnique=pset(255)
    outSAMattributes=pset("Standard")
    outSAMattrRGline=pset(None)
    outSAMattrIHstart=pset(1)
    outSAMfilter=pset(None)
    outSAMflagAND=pset(65535)
    outSAMflagOR=pset(0)
    outSAMheaderCommentFile=pset(None)
    outSAMheaderHD=pset(None)
    outSAMheaderPG=pset(None)
    outSAMmode=pset("Full")
    outSAMprimaryFlag=pset("OneBestScore")
    outSAMreadID=pset("Standard")
    outSAMstrandField=pset(None)
    outSAMorder=pset("Paired")
    outSAMmultNmax=pset(-1)
    outSAMtype=pset("SAM")
    outSAMunmapped=pset(None)
    outStd=pset("Log")
    outTmpDir=pset("")
    outWigNorm=pset("RPM")
    outWigReferencesPrefix=pset(None)
    outWigStrand=pset("Stranded")
    outWigType=pset("")
    parametersFiles=pset(None)
    quantMode=pset(None)
    quantTranscriptomeBAMcompression=pset(1)
    quantTranscriptomeBan=pset("IndelSoftclipSingleend")
    readFilesCommand=pset(None)
    readMapNumber=pset(-1)
    readMatesLengthsIn=pset("NotEqual")
    readNameSeparator=pset("/")
    runRNGseed=pset(777)
    runThreadN=pset(1)
    scoreDelOpen=pset(-2)
    scoreDelBase=pset(-2)
    scoreGap=pset(0)
    scoreGapATAC=pset(-8)
    scoreGapGCAG=pset(-4)
    scoreGapNoncan=pset(-8)
    scoreGenomicLengthLog2scale=pset(-0.25)
    scoreInsBase=pset(-2)
    scoreInsOpen=pset(-2)
    scoreStitchSJshift=pset(1)
    seedMultimapNmax=pset(10000)
    seedSearchStartLmax=pset(50)
    seedSearchStartLmaxOverLread=pset(1.0)
    seedSearchLmax=pset(0)
    seedPerReadNmax=pset(1000)
    seedPerWindowNmax=pset(50)
    seedNoneLociPerWindow=pset(10)
    sysShell=pset("/bin/sh")
    spelist=pset(False)
    winFlankNbins=pset(4)
    winAnchorDistNbins=pset(9)
    winAnchorMultimapNmax=pset(50)
    winBinNbits=pset(16)
    winReadCoverageBasesMin=pset(0)
    winReadCoverageRelativeMin=pset(0.5)
    multipleSample=pset(False)
    twopass1readsN =pset(-1)
    twopassMode=pset("")
    starversion=pset(None)
    chimOutJunctionFormat=pset(1)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"starAlign")) as f:
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
    def handleInputsoutputDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("outputDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsgenomeDir(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("genomeDir", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsreadFilesIn(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("readFilesIn", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputssampleTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("sampleTrigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsstarVersion(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("starVersion", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue="/data"
        if hasattr(self,"outputDir"):
            outputValue=getattr(self,"outputDir")
        self.send("outputDir", outputValue)
        outputValue="/data/GenomeDir"
        if hasattr(self,"genomeDir"):
            outputValue=getattr(self,"genomeDir")
        self.send("genomeDir", outputValue)
        outputValue=None
        if hasattr(self,"starVersion"):
            outputValue=getattr(self,"starVersion")
        self.send("starVersion", outputValue)
