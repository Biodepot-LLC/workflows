#!/usr/bin/python3
#lhhung 013119 - cleaned up code from Dimitar Kumar
#lhhung 031019 - added timing code
#lhhung 121119 - added and modified code from XingZhi Nui using pubsub
import os
import sys
import json
import glob
import boto3
from botocore.errorfactory import ClientError
import threading
import re
import pathlib
import datetime,time, subprocess
import os
from timeit import default_timer as timer
from dateutil.parser import *
import concurrent.futures

#globals to determine when functions have started and finished
gfunctionStartTimes={}
gfunctionFinishTimes={}
gmessagePublished={}
gErrors={}
gsplitFileSeen={}

def publish(snsClient,topicId,attr):
    snsClient.publish(TopicArn=topicId,Message='start',MessageAttributes=attr)
        
def findUnPublishedMessages(splitFiles):
    output=[]
    for splitFile in splitFiles:
        if splitFile not in gmessagePublished:
            output.append(splitFile)
    return output

def clearDirectoryFiles(bucket,directory):
    #normpath strips last /
    directory=os.path.normpath(directory)
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(bucket)
    for obj in s3bucket.objects.filter(Prefix=directory):
        s3.Object(bucket,obj.key).delete()
    
def getDirectoryFiles(bucket,directory,suffix=None):
    #make sure that the directory has no double slash but ends in single dash
    files=[]
    directory=os.path.normpath(directory+"/")
    s3 = boto3.resource('s3')
    s3bucket= s3.Bucket(bucket)
    if suffix == None:
        for obj in s3bucket.objects.filter(Prefix=directory):
            files.append(obj.key)
    else:
        for obj in s3bucket.objects.filter(Prefix=directory):
            filename=obj.key
            if filename.endswith(suffix):
                files.append(filename)
    return files
    
def getErrors(bucket,errorDir):
    errorFiles=getDirectoryFiles(bucket,errorDir)
    for errorFile in errorFiles:
        errType=os.path.dirname(errorFile)
        splitFile=os.path.basename(errorFile)
        gErrors[splitFile]=errType
    return len(errorFiles) != 0
             
def getBaseDirectoryFiles(bucket,directory,suffix=None):
    files=getDirectoryFiles(bucket,directory,suffix)
    baseFiles=[]
    if files:
        for myfile in files:
            baseFiles.append(os.path.basename(myfile))
    return baseFiles
            
def checkFinishFile(splitFile,baseFinishFiles):
    splitStem=pathlib.Path(splitFile).stem
    safFile=splitStem+".saf"
    return (safFile in baseFinishFiles)

def checkFinishFiles(splitFiles,baseFinishFiles):
    for splitFile in splitFiles:
        if not checkFinishFile(splitFile,baseFinishFiles):
            return False
            
def object_present(bucket,path):
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=bucket, Key=path)
        return True
    except ClientError:
        return False
        
def checkAllFunctionsStarted(splitFiles,bucketName,startDir,finishDir):
    startFiles=getBaseDirectoryFiles(bucketName,startDir)
    finishFiles=getBaseDirectoryFiles(bucketName,finishDir)
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if splitFile not in gsplitFileSeen and baseSplitFile not in startFiles and not checkFinishFile(baseSplitFile,finishFiles):
            return False
    return True
    
def checkAllFunctionsFinished(splitFiles,bucketName,finishDir):
    finishFiles=getBaseDirectoryFiles(bucketName,finishDir)
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if splitFile not in gfunctionFinishTimes and not checkFinishFile(baseSplitFile,finishFiles):
            return False
    return True
    
def checkAllResultsTransferred(splitFiles,bucketName,finishDir):
    finishFiles=getBaseDirectoryFiles(bucketName,finishDir)
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if not checkFinishFile(baseSplitFile,finishFiles):
            return False
    return True

def listFunctionsNotStarted(splitFiles,bucketName,startDir,finishDir,verbose=False):
    startFiles=getBaseDirectoryFiles(bucketName,startDir)
    finishFiles=getBaseDirectoryFiles(bucketName,finishDir)
    nStarted=0
    unStartedFiles=[]
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if splitFile not in gsplitFileSeen and baseSplitFile not in startFiles and not checkFinishFile(baseSplitFile,finishFiles):
            if verbose:
                sys.stderr.write("{} not started\n".format(splitFile))
            unStartedFiles.append(splitFile)
        else:
            nStarted=nStarted+1
    sys.stderr.write("{} of {} functions started\n".format(nStarted,len(splitFiles)))
    return unStartedFiles

def listFunctionsNotFinished(splitFiles,bucketName,startDir,finishDir,verbose=False):
    finishFiles=getBaseDirectoryFiles(bucketName,finishDir)
    nFinished=0
    unFinishedFiles=[]
    if verbose:
        startFiles=getBaseDirectoryFiles(bucketName,startDir)
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if splitFile not in gfunctionFinishTimes and not checkFinishFile(baseSplitFile,finishFiles):
            if verbose:
                sys.stderr.write("{} not finished\n".format(splitFile))
            unFinishedFiles.append(splitFile)
        else:
            if verbose:
                sys.stderr.write("{} ".format(splitFile))
                if splitFile in gsplitFileSeen:
                    sys.stderr.write("seen ")
                if baseSplitFile in startFiles:
                    sys.stderr.write("started ")
                if checkFinishFile(baseSplitFile,finishFiles):
                    sys.stderr.write("finished ")
                if splitFile in gfunctionFinishTimes:
                    sys.stderr.write("finish Time ")
                sys.stderr.write("\n")
            nFinished=nFinished+1
    sys.stderr.write("{} of {} functions finished\n".format(nFinished,len(splitFiles)))   
    return unFinishedFiles
    
def listFunctionsNotTransferred(splitFiles,bucketName,startDir,finishDir,verbose=False):
    finishFiles=getBaseDirectoryFiles(bucketName,finishDir)
    if verbose:
        startFiles=getBaseDirectoryFiles(bucketName,startDir)
    nFinished=0
    unFinishedFiles=[]
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if not checkFinishFile(baseSplitFile,finishFiles):
            if verbose:
                sys.stderr.write("{} not transferred\n".format(splitFile))
            unFinishedFiles.append(splitFile)
        else:
            if verbose:
                sys.stderr.write("{} ".format(splitFile))
                if splitFile in gsplitFileSeen:
                    sys.stderr.write("seen ")
                if baseSplitFile in startFiles:
                    sys.stderr.write("started ")
                if checkFinishFile(baseSplitFile,finishFiles):
                    sys.stderr.write("finished ")
                if splitFile in gfunctionFinishTimes:
                    sys.stderr.write("finish Time ")
                sys.stderr.write("\n")
            nFinished=nFinished+1
    sys.stderr.write("{} of {} results transferred \n".format(nFinished,len(splitFiles)))   
    return unFinishedFiles


def waitOnFunctionsStart(splitFiles,bucket,startDir,finishDir,sqsclient,subscription_name,interval=1,startTimeout=20,finishTimeout=100):
    waitStartTime=timer()
    unFinishedFiles=splitFiles
    unStartedFiles=splitFiles
    interval=10
    intervalTime=timer()
    while (not checkAllFunctionsStarted(unStartedFiles,bucket,startDir,finishDir) and (timer()-waitStartTime) <startTimeout):
        if(timer() -intervalTime > interval):
            unStartedFiles=listFunctionsNotStarted(unStartedFiles,bucket,startDir,finishDir,verbose=False)
            if unStartedFiles:
                sys.stderr.write("{} of {} remaining functions unstarted at time {}\n".format(len(unStartedFiles),len(splitFiles),timer()-waitStartTime))
            intervalTime=timer()
        time.sleep(1)
    
    if checkAllFunctionsStarted(splitFiles,bucket,startDir,finishDir):
        sys.stderr.write("{} to start all {} functions\n".format(timer()-waitStartTime,len(splitFiles)))
    unStartedFiles=listFunctionsNotStarted(splitFiles,bucket,startDir,finishDir,verbose=False)
    return unStartedFiles

def waitOnFunctionsFinish(splitFiles,bucket,startDir,finishDir,sqsclient,subscription_name,interval=1,startTimeout=20,finishTimeout=100):
    waitFinishTime=timer()
    unFinishedFiles=splitFiles
    interval=10
    intervalTime=timer()
    while (not checkAllFunctionsFinished(unFinishedFiles,bucket,finishDir)):
        if(timer() -intervalTime > interval):
            unFinishedFiles=listFunctionsNotFinished(unFinishedFiles,bucket,startDir,finishDir,verbose=False)
            sys.stderr.write("{} of {} remaining functions at time {}\n".format(len(unFinishedFiles),len(splitFiles),timer()-waitFinishTime))
            intervalTime=timer()
        time.sleep(1)
        time.sleep(1)
    if checkAllFunctionsFinished(unFinishedFiles,bucket,finishDir):
        sys.stderr.write("{} to finish all {} functions\n".format(timer()-waitFinishTime,len(splitFiles)))
    
    unFinishedFiles=listFunctionsNotFinished(unFinishedFiles,bucket,startDir,finishDir,verbose=False)
    return unFinishedFiles
   
def getSplitFilenames(bucket,baseDir,suffix):
    return getDirectoryFiles(bucket,baseDir,suffix)

def startInvoke(baseDir,splitFiles,bucket,topicId,recv_topic,uploadDir,startTimes,region,max_workers,bwa_string):
    attrList=[]
    fullUploadDir=baseDir+'/'+uploadDir
    snsClient = boto3.client('sns',region_name=str(region))
    for splitFile in splitFiles:
        attrList.append({'uploadDir':{'DataType':'String','StringValue':fullUploadDir},'bwa_string':{'DataType':'String','StringValue':bwa_string},'splitFile':{'DataType':'String','StringValue':splitFile},'bucketName':{'DataType':'String','StringValue':bucket},'baseDirectory':{'DataType':'String','StringValue':baseDir},'topicArn':{'DataType':'String','StringValue':recv_topic}})
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_submissions={executor.submit(lambda attr: publish(snsClient, topicId, attr), attr): attr for attr in attrList}

def getFullSubscriptionName(subscription_name):
    arntokens=subscription_name.split(":")
    return "https://sqs.%s.amazonaws.com/%s/%s"%(arntokens[3],arntokens[4],arntokens[5])

def cleanStart(bucket, startDir, finishDir, errorDir):
    for path in [startDir, finishDir, errorDir]:
        clearDirectoryFiles(bucket,path)        

def invokeFunctions (bucket,topicId,work_dir,cloud_aligns_dir,recv_topic,suffix,uploadDir,subscription_name,region,align_timeout,start_timeout,finish_timeout,max_workers=16,bwa_string=None,startSubDir="start"):
    sys.stderr.write("bucket is {}\n".format(bucket))
    sys.stderr.write("topicId is {}\n".format(topicId))
    sys.stderr.write("work_dir is {}\n".format(work_dir))
    sys.stderr.write("cloud_aligns_dir is {}\n".format(cloud_aligns_dir))
    sys.stderr.write("recv_topic is {}\n".format(recv_topic))
    sys.stderr.write("suffix is {}\n".format(suffix))
    sys.stderr.write("uploadDir is {}\n".format(uploadDir))            
    sys.stderr.write("subscription_name is {}\n".format(subscription_name))
    sys.stderr.write("region is {}\n".format(region))
    sys.stderr.write("align_timeout is {}\n".format(align_timeout))
    sys.stderr.write("start_timeout is {}\n".format(start_timeout))
    sys.stderr.write("finish_timeout is {}\n".format(finish_timeout))
    sys.stderr.write("bwa_string is {}\n".format(bwa_string))
    finishTimes={}
    startTimes={}
    sqsclient=boto3.client('sqs',region_name=str(region))
    splitFiles=getSplitFilenames(bucket,cloud_aligns_dir,suffix)
    start = timer()
    alignAttempts=0
    startAttempts=0
    maxAlignAttempts=2
    maxStartAttempts=2
    remainingSplitFiles=splitFiles
    startDir=os.path.join(work_dir,startSubDir)
    finishDir=os.path.join(work_dir,uploadDir)
    errorDir=os.path.join(work_dir,"error")
    clearDirectoryFiles(bucket,startDir)
    clearDirectoryFiles(bucket,finishDir)
    remainingStartFiles=splitFiles
    remainingSplitFiles=splitFiles
    
    cleanStart(bucket,startDir,finishDir,errorDir)
    while remainingStartFiles and startAttempts < maxStartAttempts:
        startInvoke(work_dir,splitFiles,bucket,topicId,recv_topic,uploadDir,startTimes,region,max_workers,bwa_string)    
        sys.stderr.write('Time elapsed for launch is {}\n'.format(timer()-start))
        fullSubscriptionName=getFullSubscriptionName(subscription_name)
        remainingStartFiles=waitOnFunctionsStart(remainingSplitFiles,bucket,startDir,finishDir,sqsclient,fullSubscriptionName,startTimeout=start_timeout,finishTimeout=finish_timeout)
        startAttempts=startAttempts+1
        if remainingStartFiles:
            for startFile in remainingStartFiles:
                sys.stderr.write("{} not started\n".format(startFile))
        else:
            sys.stderr.write('Time elapsed to start all Files is {}\n'.format(timer()-start))
    remainingSplitFiles=listFunctionsNotFinished(splitFiles,bucket,startDir,finishDir,verbose=False)
    while remainingSplitFiles and alignAttempts < maxAlignAttempts:
        startInvoke(work_dir,splitFiles,bucket,topicId,recv_topic,uploadDir,startTimes,region,max_workers,bwa_string)    
        sys.stderr.write('Time elapsed for launch is {}\n'.format(timer()-start))
        fullSubscriptionName=getFullSubscriptionName(subscription_name)
        remainingSplitFiles=waitOnFunctionsFinish(remainingSplitFiles,bucket,startDir,finishDir,sqsclient,fullSubscriptionName,startTimeout=start_timeout,finishTimeout=finish_timeout)
        alignAttempts=alignAttempts+1
        if remainingSplitFiles:
            for splitFile in remainingSplitFiles:
                sys.stderr.write("{} not finished\n".format(startFile))
        else:
            sys.stderr.write('Time elapsed to finish all Files is {}\n'.format(timer()-start))          
    #It is possible to finish but not have the files finish transferring
    while (not checkAllResultsTransferred(splitFiles,bucket,finishDir) and (timer()-start) < align_timeout):
        time.sleep(1)
    if not checkAllResultsTransferred(splitFiles,bucket,finishDir):
        listFunctionsNotTransferred(splitFiles,bucket,startDir,finishDir)
        gErrors['Transfer']="True"
    else:
        sys.stderr.write("{} to write all {} result files\n".format(timer()-start,len(splitFiles)))
    for splitFile in splitFiles:
        if splitFile in gfunctionStartTimes and splitFile in gfunctionFinishTimes:
            sys.stderr.write("{} {} {} {}\n".format(splitFile,gfunctionStartTimes[splitFile],gfunctionFinishTimes[splitFile],gfunctionFinishTimes[splitFile]-gfunctionStartTimes[splitFile]))
    for remainingSplitFile in remainingSplitFiles:
        sys.stderr.write("Did not finish {}\n".format(remainingSplitFile))
    for splitFile in splitFiles:
        if splitFile in gErrors:
            sys.stderr.write("Error for {} - {}\n".format(splitFile,gErrors[splitFile]))
    getErrors(bucket,errorDir)
    if gErrors:
        sys.stderr.write("errors {}\n".format(gErrors))
        raise Exception ("Errors detected during the alignment phase")
    
if __name__ == "__main__":
    if len(sys.argv) != 14 :
        exit(0)
    bucket=sys.argv[1]
    topicId=sys.argv[2]
    work_dir=sys.argv[3]
    cloud_aligns_dir=argv[4]
    recv_topic=sys.argv[5]
    suffix=sys.argv[6]
    uploadDir=sys.argv[7]
    subscription_name=sys.argv[8]
    max_workers=sys.argv[9]
    region=sys.argv[10]
    align_timeout=argv[11]
    start_timeout=argv[12]
    finish_timeout=argv[13]
    bwa_string=argv[14]
    
    invokeFunctions(bucket,topicId,work_dir,cloud_aligns_dir,recv_topic,suffix,uploadDir,subscription_name,region,align_timeout,start_timeout,finish_timeout,max_workers=max_workers,bwa_string=bwa_string,startSubDir="start")
