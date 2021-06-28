#!/usr/local/bin/python3
#lhhung 013119 - cleaned up code from Dimitar Kumar
#lhhung 031019 - added timing code
#lhhung 020820 - generalized and modifed XingZhi Nui pubsub code to use Python API

import os
import sys
from google.cloud import pubsub
from google.cloud import storage
import base64
import datetime,time
from timeit import default_timer as timer
import concurrent.futures
import google.api_core.exceptions
import pathlib

#globals to determine when functions have started and finished
gfunctionStartTimes={}
gfunctionFinishTimes={}
gmessagePublished={}
greInvoke={}
gsplitFileSeen={}

def get_callback(f, data,futures,dataHash):
    def callback(f):
        try:
            dataHash[data]=f.result()
            futures.pop(data)
        except:  # noqa
            sys.stderr.write("Invoke error for {} for {}\n".format(f.exception(), data))
    return callback

def publish(publisher,topic_path,message,splitFile,bucketName,baseDir,recv,uploadDir,project_id,bwa_string,futures):
    data = base64.b64encode(message)
    # When you publish a message, the client returns a future.
    future=publisher.publish(topic_path,data,splitFile=splitFile,bucketName=bucketName,baseDirectory=baseDir,recv=recv,uploadDir=uploadDir,project_id=project_id,bwa_string=bwa_string)
    futures[splitFile]=future
    future.add_done_callback(get_callback(future, splitFile,futures,gmessagePublished))

def waitOnMessages(futures,timeout):
    startTime=timer()
    while futures and timer()-startTime < timeout:
        time.sleep(1)
    return futures


def findUnPublishedMessages(splitFiles):
    output=[]
    for splitFile in splitFiles:
        if splitFile not in gmessagePublished:
            output.append(splitFile)
    return output

def getDirectoryFiles(storageClient,bucketName,directory):
    files=[]
    for blob in storageClient.list_blobs(bucketName, prefix=directory):
        files.append(os.path.basename(blob.name))
    return files
    
def checkFinishFile(baseSplitFile,finishFiles):
    splitStem=pathlib.Path(baseSplitFile).stem
    safFile=splitStem+".saf"
    return (safFile in finishFiles)

def checkFinishFiles(splitFiles,finishFiles):
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if not checkFinishFile(baseSplitFile,finishFiles):
            return False

def checkAllFunctionsStarted(splitFiles,storageClient,bucketName,workDir,uploadDir):
    startDir=os.path.join(workDir,"start")
    finishDir=os.path.join(workDir,uploadDir)
    startFiles=getDirectoryFiles(storageClient,bucketName,startDir)
    finishFiles=getDirectoryFiles(storageClient,bucketName,finishDir)
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if baseSplitFile not in gsplitFileSeen:
            if baseSplitFile in startFiles or checkFinishFile(baseSplitFile,finishFiles):
                gsplitFileSeen[baseSplitFile]=True
            else:
                return False
    return True
    
def checkAllFunctionsFinished(splitFiles,storageClient,bucketName,workDir,uploadDir):
    finishDir=os.path.join(workDir,uploadDir)
    finishFiles=getDirectoryFiles(storageClient,bucketName,finishDir)
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if baseSplitFile not in gfunctionFinishTimes and not checkFinishFile(baseSplitFile,finishFiles):
            return False
    return True
        
def listFunctionsNotStarted(splitFiles,bucketName,workDir,uploadDir,verbose=False):
    storageClient=storage.Client()
    startDir=os.path.join(workDir,"start")
    finishDir=os.path.join(workDir,uploadDir)
    startFiles=getDirectoryFiles(storageClient,bucketName,startDir)
    finishFiles=getDirectoryFiles(storageClient,bucketName,finishDir)
    nStarted=0
    unStartedFiles=[]
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if baseSplitFile not in gsplitFileSeen and baseSplitFile not in startFiles and not checkFinishFile(baseSplitFile,finishFiles):
            if verbose:
                sys.stderr.write("{} not started\n".format(splitFile))
            unStartedFiles.append(splitFile)
        else:
            nStarted=nStarted+1
    sys.stderr.write("{} of {} functions started\n".format(nStarted,len(splitFiles)))
    return unStartedFiles
    
def listFunctionsNotFinished(splitFiles,bucketName,workDir,uploadDir,verbose=False):
    storageClient=storage.Client()
    startDir=os.path.join(workDir,"start")
    finishDir=os.path.join(workDir,uploadDir)
    startFiles=getDirectoryFiles(storageClient,bucketName,startDir)
    finishFiles=getDirectoryFiles(storageClient,bucketName,finishDir)
    nFinished=0
    unFinishedFiles=[]
    for splitFile in splitFiles:
        baseSplitFile=os.path.basename(splitFile)
        if baseSplitFile not in gfunctionFinishTimes and not checkFinishFile(baseSplitFile,finishFiles):
            if verbose:
                sys.stderr.write("{} not finished\n".format(splitFile))
            unFinishedFiles.append(splitFile)
        else:
            if verbose:
                sys.stderr.write("{} ".format(splitFile))
                if baseSplitFile in gsplitFileSeen:
                    sys.stderr.write("seen ")
                if baseSplitFile in startFiles:
                    sys.stderr.write("started ")
                if checkFinishFile(baseSplitFile,finishFiles):
                    sys.stderr.write("finished ")
                if baseSplitFile in gfunctionFinishTimes:
                    sys.stderr.write("finish Time ")
                sys.stderr.write("\n")
            nFinished=nFinished+1
    sys.stderr.write("{} of {} functions finished\n".format(nFinished,len(splitFiles)))   
    return unFinishedFiles
     
def execute(cmd):
    print("{}".format(cmd))
    output=os.popen(cmd)
    ret=output.read().strip()
    return ret
    
def processing_data(splitFiles):
    for splitFile in splitFiles:
        if splitFile not in gfunctionStartTimes and splitFile not in gfunctionFinishTimes: 
            return True
    return False

def recv_callback(message,publisher,topic_path,bucket,baseDir,recv_topic,fullUploadDir,project_id,futures,maxReInvoke=2,verbose=False):
    errorState=False
    if message is None:
        return
    if message.attributes:
        splitFile=message.attributes.get("splitFile")
        baseSplitFile = os.path.basename(splitFile)
        gsplitFileSeen[baseSplitFile]=True
        stage=message.attributes.get("stage")
        if message.attributes.get('error') == '1':
            if baseSplitFile not in greInvoke:
                greInvoke[baseSplitFile]=0
            if greInvoke[baseSplitFile] > maxReInvoke:
                errorState=True
                gfunctionStartTimes[baseSplitFile]=1
                gfunctionFinishTimes[baseSplitFile]=1
                sys.stderr.write("{} - {} retries - giving up\n".format(stage,greInvoke[baseSplitFile]))
            else:
                sys.stderr.write("{} - {} retries - trying again\n".format(stage,greInvoke[baseSplitFile]))
                publish(publisher,topic_path,b"start",splitFile,bucket,baseDir,recv_topic,fullUploadDir,project_id,futures)
                greInvoke[baseSplitFile]+=1
        else:
            if stage =="start":
                gfunctionStartTimes[baseSplitFile]=message.publish_time
            elif stage =="finish":
                gfunctionFinishTimes[baseSplitFile]=message.publish_time
        if verbose:
            print("Attributes:")
            for key in message.attributes:
                value = message.attributes.get(key)
                print("{}: {}".format(key, value))        
    message.ack()
    return errorState

def delete_subscription(client,path):
    try:
        client.delete_subscription(path)
    except: # noqa
        sys.stderr.write("no existing subscription {}\n".format(path))

        
def create_subscription(client,subscription_path,topic_path):
    #must delete any existing subscription in case the topic it is subscribed to is deleted or it will not properly subscribe even if the topic is recreated
    delete_subscription(client,subscription_path)
    return client.create_subscription(subscription_path,topic_path)    

def clear_queue(project_id,topic,timeout=10):
    waitStartTime=timer()
    client = pubsub.SubscriberClient() 
    subscription_path = client.subscription_path(project_id, topic)
    topic_path = client.topic_path(project_id, topic)
    #must delete any existing subscription in case the topic it is subscribed to is deleted or it will not properly subscribe even if the topic is recreated
    delete_subscription(client,subscription_path)
    client.create_subscription(subscription_path,topic_path)   
    while (timer()-waitStartTime < timeout):
        streaming_pull_future = client.subscribe(subscription_path,callback=None)
        try:
            if streaming_pull_future:
                print(streaming_pull_future.result(timeout=10))
        except: # noqa
            streaming_pull_future.cancel()
            
def waitOnFunctions(splitFiles,recv_topic,project_id,bucket,topicId, work_dir,alignsDir,uploadDir,startTimeout,finishTimeout,checkInterval=30):
    reinvokeFutures={}
    waitStartTime=timer()
    #for reinvoke
    publisher = pubsub.PublisherClient()
    topic_path=createTopic(publisher,project_id,topicId)
    fullUploadDir=os.path.join(work_dir,uploadDir)
    #create client to read/write to pubsub queue 
    client = pubsub.SubscriberClient()
    subscription_path = client.subscription_path(project_id, recv_topic)
    recv_path = client.topic_path(project_id, recv_topic)
    create_subscription(client,subscription_path,recv_path)
    storageClient=storage.Client()
    waitIntervalTime=timer()
    unstartedSplitFiles=splitFiles
    #wait on start
    while (not checkAllFunctionsStarted(unstartedSplitFiles,storageClient,bucket,work_dir,uploadDir) and timer()-waitStartTime < startTimeout):
        streaming_pull_future = client.subscribe(subscription_path,callback=lambda message: recv_callback(message,publisher,topic_path,bucket,work_dir,recv_topic,fullUploadDir,project_id,reinvokeFutures))
        try:
            if streaming_pull_future:
                streaming_pull_future.result(timeout=10)
        except: # noqa
            streaming_pull_future.cancel()
            if timer()-waitIntervalTime > checkInterval:
                sys.stderr.write("Checking start functions at time (queue empty) {}\n".format(timer()-waitStartTime))
                waitIntervalTime=timer()
                unstartedSplitFiles=listFunctionsNotStarted(unstartedSplitFiles,bucket,work_dir,uploadDir)
    if unstartedSplitFiles:
        for unstartedSplitFile in unstartedSplitFiles:
            sys.stderr.write('{} not started\n'.format(unstartedSplitFile))
        return unstartedSplitFiles
    else:
        sys.stderr.write('Time after last message for functions to start is {}\n'.format(timer()-waitStartTime))
    unfinishedSplitFiles=listFunctionsNotFinished(splitFiles,bucket,work_dir,uploadDir)
    #wait on Finish
    while (not checkAllFunctionsFinished(unfinishedSplitFiles,storageClient,bucket,work_dir,uploadDir) and timer()-waitStartTime < finishTimeout):
        streaming_pull_future = client.subscribe(subscription_path,callback=lambda message: recv_callback(message,publisher,topic_path,bucket,work_dir,recv_topic,fullUploadDir,project_id,reinvokeFutures))
        try:
            if streaming_pull_future:
                streaming_pull_future.result(timeout=10)
        except: # noqa
            streaming_pull_future.cancel()
            if timer()-waitIntervalTime > checkInterval:
                sys.stderr.write("Checking finish functions at time (queue empty) {}\n".format(timer()-waitStartTime))
                waitIntervalTime=timer()
                unfinishedSplitFiles=listFunctionsNotFinished(unfinishedSplitFiles,bucket,work_dir,uploadDir)
        #This checks on errors and retries if there is an error
        waitOnMessages(reinvokeFutures,10)
    if unfinishedSplitFiles:
        for unfinishedSplitFile in unfinishedSplitFiles:
            sys.stderr.write('{} not finished\n'.format(unfinishedSplitFile))        
    else:
        sys.stderr.write('Time after last message for functions to finish is {}\n'.format(timer()-waitStartTime))        
    return unfinishedSplitFiles
def waitOnFunctionsStart(splitFiles,recv_topic,project_id,bucket,topicId, work_dir,alignsDir,uploadDir,startTimeout,finishTimeout,checkInterval=30):
    reinvokeFutures={}
    waitStartTime=timer()
    #for reinvoke
    publisher = pubsub.PublisherClient()
    topic_path=createTopic(publisher,project_id,topicId)
    fullUploadDir=os.path.join(work_dir,uploadDir)
    #create client to read/write to pubsub queue 
    client = pubsub.SubscriberClient()
    subscription_path = client.subscription_path(project_id, recv_topic)
    recv_path = client.topic_path(project_id, recv_topic)
    create_subscription(client,subscription_path,recv_path)
    storageClient=storage.Client()
    waitIntervalTime=timer()
    unstartedSplitFiles=splitFiles
    #unstartedSplitFiles=listFunctionsNotStarted(splitFiles,bucket,work_dir,uploadDir)
    #wait on start
    while (not checkAllFunctionsStarted(unstartedSplitFiles,storageClient,bucket,work_dir,uploadDir) and timer()-waitStartTime < startTimeout):
        streaming_pull_future = client.subscribe(subscription_path,callback=lambda message: recv_callback(message,publisher,topic_path,bucket,work_dir,recv_topic,fullUploadDir,project_id,reinvokeFutures))
        try:
            if streaming_pull_future:
                streaming_pull_future.result(timeout=10)
        except: # noqa
            streaming_pull_future.cancel()
            if timer()-waitIntervalTime > checkInterval:
                sys.stderr.write("Checking start functions at time (queue empty) {}\n".format(timer()-waitStartTime))
                waitIntervalTime=timer()
                unstartedSplitFiles=listFunctionsNotStarted(unstartedSplitFiles,bucket,work_dir,uploadDir)
    unstartedSplitFiles=listFunctionsNotStarted(unstartedSplitFiles,bucket,work_dir,uploadDir)            
    if unstartedSplitFiles:
        for unstartedSplitFile in unstartedSplitFiles:
            sys.stderr.write('{} not started\n'.format(unstartedSplitFile))
        else:
            sys.stderr.write('Time after last message for functions to start is {}\n'.format(timer()-waitStartTime))
    return unstartedSplitFiles

def waitOnFunctionsFinish(splitFiles,recv_topic,project_id,bucket,topicId, work_dir,alignsDir,uploadDir,startTimeout,finishTimeout,checkInterval=30):
    reinvokeFutures={}
    waitStartTime=timer()
    #for reinvoke
    publisher = pubsub.PublisherClient()
    topic_path=createTopic(publisher,project_id,topicId)
    fullUploadDir=os.path.join(work_dir,uploadDir)
    #create client to read/write to pubsub queue 
    client = pubsub.SubscriberClient()
    subscription_path = client.subscription_path(project_id, recv_topic)
    recv_path = client.topic_path(project_id, recv_topic)
    create_subscription(client,subscription_path,recv_path)
    storageClient=storage.Client()
    waitIntervalTime=timer()
    unfinishedSplitFiles=listFunctionsNotFinished(splitFiles,bucket,work_dir,uploadDir)
    while (not checkAllFunctionsFinished(unfinishedSplitFiles,storageClient,bucket,work_dir,uploadDir) and timer()-waitStartTime < finishTimeout):
        streaming_pull_future = client.subscribe(subscription_path,callback=lambda message: recv_callback(message,publisher,topic_path,bucket,work_dir,recv_topic,fullUploadDir,project_id,reinvokeFutures))
        try:
            if streaming_pull_future:
                streaming_pull_future.result(timeout=10)
        except: # noqa
            streaming_pull_future.cancel()
            if timer()-waitIntervalTime > checkInterval:
                sys.stderr.write("Checking finish functions at time (queue empty) {}\n".format(timer()-waitStartTime))
                waitIntervalTime=timer()
                unfinishedSplitFiles=listFunctionsNotFinished(unfinishedSplitFiles,bucket,work_dir,uploadDir)
        #This checks on errors and retries if there is an error
        waitOnMessages(reinvokeFutures,10)
    if unfinishedSplitFiles:
        for unfinishedSplitFile in unfinishedSplitFiles:
            sys.stderr.write('{} not finished\n'.format(unfinishedSplitFile))        
    else:
        sys.stderr.write('Time after last message for functions to finish is {}\n'.format(timer()-waitStartTime))        
    return unfinishedSplitFiles


def get_blobs_with_prefix_suffix(bucket_name, prefix, suffix, delimiter=None):
    returnBlobs=[]
    storage_client = storage.Client() 
    blobs = storage_client.list_blobs(
        bucket_name, prefix=prefix, delimiter=delimiter
    )
    for blob in blobs:
        if pathlib.Path(blob.name).suffix == suffix:
            returnBlobs.append(blob.name)
    return returnBlobs
    
def getSplitFilenames(bucket,workDir,alignsDir,suffix):
    splitFiles=get_blobs_with_prefix_suffix(bucket,alignsDir,suffix)
    sys.stderr.write("found {} files from bucket {} alignsDir {} suffix {}\n".format(len(splitFiles),bucket,alignsDir,suffix))
    return splitFiles

def createTopic(publisher,project_id,topic_id):
    topic_path = publisher.topic_path(project_id, topic_id)
    try:
        publisher.create_topic(topic_path)
    except google.api_core.exceptions.AlreadyExists:
        sys.stderr.write("topic {} already exists\n".format(topic_id))
    return topic_path
           
def startInvoke(project_id,work_dir,alignsDir,splitFiles,bucket,topicId,recv_topic,uploadDir,bwa_string,max_workers,maxAttempts=2,clearQueue=True):
    fullUploadDir=os.path.join(work_dir,uploadDir)
    #create client to read/write to pubsub queue 
    batch_settings = pubsub.types.BatchSettings(max_bytes=1024, max_latency=1)
    publisher = pubsub.PublisherClient(batch_settings)
    sys.stderr.write("creating topic if it does not exist\n")
    topic_path=createTopic(publisher,project_id,topicId)
    sys.stderr.write("creating recv_topic if it does not exist\n")
    createTopic(publisher,project_id,recv_topic)
    if clearQueue:
        sys.stderr.write("clearing queue\n")
        clear_queue(project_id,recv_topic)
        sys.stderr.write("cleared queue\n")
    attempts=0
    publishStartTime=timer()
    publishTimeout=30
    mySplitFiles=splitFiles
    maxAttempts=1
    while mySplitFiles and attempts < maxAttempts:
        if attempts > 0:
            sys.stderr.write("splitFiles {} remain\nRetry {}\n".format(mySplitFiles,attempts))
        if int(max_workers) > len(mySplitFiles):
            max_workers=len(mySplitFiles)
        sys.stderr.write("invoking with {} workers\n".format(max_workers))
        invokeFutures={}
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(max_workers)) as executor:
            future={executor.submit(publish,publisher,topic_path,b"start",splitFile,bucket,work_dir,recv_topic,fullUploadDir,project_id,bwa_string,invokeFutures): splitFile for splitFile in mySplitFiles}
        waitOnMessages(invokeFutures,publishTimeout)
        mySplitFiles=findUnPublishedMessages(mySplitFiles)
        attempts=attempts+1
    sys.stderr.write("Time to publish messages {}\n".format(timer()-publishStartTime))
    return mySplitFiles
       
def invokeFunctions (bucket,topicId,work_dir,aligns_dir,recv_topic,suffix,uploadDir,project_id,max_workers,startTimeout,finishTimeout,bwa_string="bwa aln "):
    sys.stderr.write("bucket is {}\n".format(bucket))
    sys.stderr.write("topicId is {}\n".format(topicId))
    sys.stderr.write("work_dir is {}\n".format(work_dir))
    sys.stderr.write("aligns_dir is {}\n".format(aligns_dir))
    sys.stderr.write("recv_topic is {}\n".format(recv_topic))
    sys.stderr.write("suffix is {}\n".format(suffix))
    sys.stderr.write("uploadDir is {}\n".format(uploadDir))            
    sys.stderr.write("project_id is {}\n".format(project_id))
    sys.stderr.write("max_workers is {}\n".format(max_workers))
    sys.stderr.write("start timeout is {}\n".format(startTimeout))
    sys.stderr.write("finish timeout is {}\n".format(finishTimeout))
    sys.stderr.write("bwa string is {}\n".format(bwa_string))
    finishTimes={}
    startTimes={}
    splitFiles=getSplitFilenames(bucket,work_dir,aligns_dir,suffix)
    #splitFiles=splitFiles[0:2]
    start = timer()
    maxStartAttempts=2
    maxAlignAttempts=2
    alignAttempts=0
    startAttempts=0
    sys.stderr.write("Working on files {}\n".format(splitFiles))
    startFiles=splitFiles
    while startFiles and startAttempts < maxStartAttempts:
        unqueuedFiles=startInvoke(project_id,work_dir,aligns_dir,startFiles,bucket,topicId,recv_topic,uploadDir,bwa_string,max_workers,clearQueue=(startAttempts==0))
        if unqueuedFiles:
            sys.stderr.write("unable to put {} onto the start message queue\n".format(unqueuedFiles))
        sys.stderr.write('Time elapsed for launch is {}\n'.format(timer()-start))
        startFiles=waitOnFunctionsStart(startFiles,recv_topic,project_id,bucket,topicId, work_dir,aligns_dir,uploadDir,startTimeout,finishTimeout)
        startAttempts=startAttempts+1
    while splitFiles and alignAttempts < maxAlignAttempts:
        if alignAttempts > 0:
            unqueuedFiles=startInvoke(project_id,work_dir,aligns_dir,splitFiles,bucket,topicId,recv_topic,uploadDir,bwa_string,max_workers,clearQueue=False)
            if unqueuedFiles:
                sys.stderr.write("unable to put {} onto the start message queue\n".format(unqueuedFiles))
        sys.stderr.write('Time elapsed for launch is {}\n'.format(timer()-start))
        splitFiles=waitOnFunctionsFinish(splitFiles,recv_topic,project_id,bucket,topicId, work_dir,aligns_dir,uploadDir,startTimeout,finishTimeout)
        alignAttempts=alignAttempts+1                
    sys.stderr.write('Time elapsed for align is {}\n'.format(timer()-start))

if __name__ == "__main__":
    if len(sys.argv) != 14:
        sys.stderr.write("missing argument\n")
        raise
    bucket=sys.argv[1]
    topicId=sys.argv[2]
    work_dir=sys.argv[3]
    aligns_dir=sys.argv[4]
    recv_topic=sys.argv[5]
    suffix=sys.argv[6]
    uploadDir=sys.argv[7]
    project_id=sys.argv[8]
    max_workers=sys.argv[9]
    credentials_file=sys.argv[10]
    startTimeout=int(sys.argv[11])
    finishTimeout=int(sys.argv[12])
    bwa_string=int(sys.argv[13])
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
    invokeFunctions(bucket,topicId,work_dir,aligns_dir,recv_topic,suffix,uploadDir,project_id,max_workers,startTimeout,finishTimeout,bwa_string=bwa_string)
