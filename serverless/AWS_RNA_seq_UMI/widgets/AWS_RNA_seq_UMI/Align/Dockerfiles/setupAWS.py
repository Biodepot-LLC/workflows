#!/usr/local/bin/python
#lhhung 121119 - converted XingZhi's cli setup code to boto3 and added some error check
#add bwa flag generation

import boto3
import os,yaml,re,time,json, argparse,sys
from invokeAWS import invokeFunctions

#global clients - boto3 not threadsafe
sns_client=None
sqs_client=None

def execute(cmd):
    print("{}".format(cmd))
    output=os.popen(cmd)
    ret=output.read().strip()
    return ret
    
def get_bwa_string():
	bwa_string=""
	#flags with string or int values
	numerical_flags=['n']
	valued_flags=['o','e','i','d','l','k','m','t','M','O','E','R','q']
	boolean_flags=['L','N']
	for flag in numerical_flags+valued_flags:
		env_var='bwa_'+flag
		if env_var in os.environ:
			bwa_string = bwa_string + "-{} {} ".format(flag,os.environ.get(env_var))
	for flag in boolean_flags:
		env_var='bwa_'+flag
		if env_var in os.environ:
			bwa_string = bwa_string + "-{} ".format(flag)
	if bwa_string != "":
		return "bwa aln " + bwa_string
	return None
	
def create_topic(topic_name):
    print ("creating topic {}".format(topic_name))
    return sns_client.create_topic(Name=topic_name)['TopicArn']
    
def create_queue(queue_name):
    print("creating queue {}".format(queue_name))
    return sqs_client.create_queue(QueueName=queue_name)['QueueUrl']

def create_recv(recv_topic,recv_subscription):
    print ('creating recv queue')
    recv_topic_id=create_topic(recv_topic)
    queue_url=create_queue(recv_subscription)
    sqs_arn=recv_topic_id.replace("sns","sqs").replace(recv_topic,recv_subscription)
    sns_client.subscribe(TopicArn=recv_topic_id,Protocol='sqs',Endpoint=sqs_arn)
    queue_policy='{"Version":"2012-10-17","Id":"%s/SQSDefaultPolicy","Statement": [{"Effect": "Allow", "Principal": {"AWS": "*"},"Action":"SQS:SendMessage","Resource": "%s","Condition": {"ArnEquals":{"aws:SourceArn": "%s"}}}]}'%(sqs_arn,sqs_arn,recv_topic_id)
    sqs_client.set_queue_attributes(QueueUrl=queue_url,Attributes={'Policy':queue_policy}) 
    return recv_topic_id

def main():
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", action='store',dest="bucket_name",default="dtoxsbucket",
                    help="bucket_name, S3 bucket to store project")
    parser.add_argument("-c",action='store',dest="credentials_dir",default="/data/.aws",
                    help="credentials_dir, directory with AWS credentials")
    parser.add_argument("-t", action='store',dest="topic_name",default="dtoxspubsub",
                    help="topic_name, identifier for topic")
    parser.add_argument("-r", action='store',dest="recv_topic",default="dtoxsrecv",
                    help="recv_topic, identifier for recv_topic")
    parser.add_argument("--region", action='store',dest="region",default="us-east-1",
                    help="region")
    parser.add_argument("-s", action='store',dest="recv_subscription",default="dtoxsrecvsub",
                    help="recv_subscription, sqs queue name")
    parser.add_argument("--fn", action='store',dest="function_name",default="dtoxsfunction",
                    help="function_name, name of lambda function")
    parser.add_argument("--fastq_suffix", action='store',dest="fastq_suffix",default="fq",
                    help="fastq_suffix, suffix of fastq files")                 
    parser.add_argument("-w", action='store',dest="work_dir",default="dtoxsdir",
                    help="work_dir, directory in bucket where project is created")
    parser.add_argument("--aligns_dir", action='store',dest="cloud_aligns_dir",
                    help="cloud_aligns_dir, directory in bucket where split files are kept")
    parser.add_argument("--uploadDir", action='store',dest="upload_dir",default="saf",
                    help="upload_dir, directory in bucket where the lambda output is stored")
    parser.add_argument("--max_workers", type=int,action='store',dest="max_workers",default=16,
                    help="max_workers, maximum of number of threads used to publish a message")
    parser.add_argument("--align_timeout", type=int, action='store',dest="align_timeout",default=240,
                    help="align_timeout, maximum time allowed for complete alignment to finish including transfer of files")       
    parser.add_argument("--start_timeout", type=int,action='store',dest="start_timeout",default=120,
                    help="start_timeout, maximum time allowed for lambda to receive message and start processing")
    parser.add_argument("--finish_timeout", type=int,action='store',dest="finish_timeout",default=200,
                    help="finish_timeout, maximum time allowed for lambda function to finish processing")
                          
    args=parser.parse_args()
    
    credentials_dir=args.credentials_dir
    bucket_name=args.bucket_name
    region=args.region
    topic_name=args.topic_name
    recv_topic=args.recv_topic
    recv_subscription=args.recv_subscription
    function_name=args.function_name
    fastq_suffix=args.fastq_suffix
    work_dir=args.work_dir
    cloud_aligns_dir=args.cloud_aligns_dir
    upload_dir=args.upload_dir
    max_workers=args.max_workers
    align_timeout=args.align_timeout
    start_timeout=args.start_timeout
    finish_timeout=args.finish_timeout
    
    bwa_string=get_bwa_string()
    sys.stderr.write("credentials directory={}\n".format(credentials_dir))
    sys.stderr.write("bucket_name={}\n".format(bucket_name))
    sys.stderr.write("region={}\n".format(region))
    sys.stderr.write("topic_name={}\n".format(topic_name))
    sys.stderr.write("recv_topic={}\n".format(recv_topic))
    sys.stderr.write("recv_subscription={}\n".format(recv_subscription))
    sys.stderr.write("function_name={}\n".format(function_name))
    sys.stderr.write("fastq_suffix={}\n".format(fastq_suffix))
    sys.stderr.write("work_dir={}\n".format(work_dir))
    sys.stderr.write("cloud_aligns_dir={}\n".format(cloud_aligns_dir))
    sys.stderr.write("upload_dir={}\n".format(upload_dir))
    sys.stderr.write("max_workers={}\n".format(max_workers))
    sys.stderr.write("align_timeout={}\n".format(align_timeout))    
    sys.stderr.write("start_timeout={}\n".format(start_timeout))    
    sys.stderr.write("finish_timeout={}\n".format(finish_timeout))    
    sys.stderr.write("bwa_string={}\n".format(bwa_string))  
    #get bwa string

    #copy credentials
    execute('''cp -r %s/* /root/.aws/. '''%(credentials_dir))
    
    #initialize clients
    global sns_client,sqs_client
    sns_client=boto3.client('sns',region_name=str(region))
    sqs_client=boto3.client('sqs',region_name=str(region))
    
    topic_id=create_topic(topic_name)
    recv_topic_id=create_recv(recv_topic,recv_subscription)
    sqs_arn=recv_topic_id.replace("sns","sqs").replace(recv_topic,recv_subscription)
    invokeFunctions(bucket_name,topic_id,work_dir,cloud_aligns_dir,recv_topic_id,fastq_suffix,upload_dir,sqs_arn,region,align_timeout,start_timeout,finish_timeout,max_workers=max_workers,bwa_string=bwa_string)

main()
