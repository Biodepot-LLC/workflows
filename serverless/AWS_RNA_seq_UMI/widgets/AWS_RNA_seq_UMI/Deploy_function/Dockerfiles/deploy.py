#!/usr/local/bin/python
#lhhung 121119 - converted XingZhi's cli setup code to boto3 and added some error check

import boto3
import os,yaml,re,time,json, argparse,sys


#global clients - boto3 not threadsafe
sns_client=None
sqs_client=None
iam_client=None
lambda_client=None

def execute(cmd):
    print("{}".format(cmd))
    output=os.popen(cmd)
    ret=output.read().strip()
    return ret

def create_topic(topic_name):
    print ("creating topic {}".format(topic_name))
    return sns_client.create_topic(Name=topic_name)['TopicArn']
    
def create_role_arn(role_name,topic_id):
    return "arn:aws:iam::{}:role/{}".format(topic_id.split(':')[-2],role_name)

def create_role(role_name,policy_string,topic_id):
    #cannot use waiter without role policy but cannot create role policy without role
    try:
        ret=iam_client.create_role(RoleName=role_name,AssumeRolePolicyDocument=policy_string)
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("role already exists - using existing role")
        return create_role_arn(role_name,topic_id)
    return ret["Role"]["Arn"]

	    
def create_role_policy(role_name,policy_name,policy_document):
    return iam_client.put_role_policy(RoleName=role_name,PolicyName=policy_name,PolicyDocument=policy_document)
    
def deploy_function(topic_id,topic_name,function_name,function_zipfile,handler,memory,timeout,policy_name,role_name,user_id):
    print("creating role")
    role_arn=create_role(role_name,'{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":["lambda.amazonaws.com","ec2.amazonaws.com","apigateway.amazonaws.com","events.amazonaws.com"]},"Action":["sts:AssumeRole"]}]}',topic_id)    
    print("creating role policy")
    create_role_policy(role_name,policy_name,'{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": "s3:*","Resource": "*"},{"Effect": "Allow","Action":"sns:Publish","Resource": "*"},{"Effect": "Allow","Action": ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],"Resource": "arn:aws:logs:*:*:*"}]}')
    #delete if function exists
    try:
        lambda_client.delete_function(FunctionName=function_name)
        sys.stderr.write("existing function {} deleted\n".format(function_name))
    except Exception as e:
        sys.stderr.write("function {} does not yet exist\n".format(function_name))
    
    #retry as it takes time for the policy to become active
    print("creating lambda function")
    with open (function_zipfile, 'rb') as f:
        code=f.read() 
    retries=0
    ret=None
    while retries < 20:
        try:
            ret=lambda_client.create_function(FunctionName=function_name,Runtime='python3.7',Role=role_arn,Handler=handler,
            Timeout=timeout,MemorySize=memory,Code={'ZipFile':code})
            sys.stderr.write("successfully created function\n")
            sys.stderr.write("return value is {}\n".format(ret))
            break
        except lambda_client.exceptions.InvalidParameterValueException as e:
            retries+=1
            sys.stderr.write("waiting for policy retry {} attempts".format(retries))
            time.sleep(5)
    function_arn=ret['FunctionArn']
    sns_client.subscribe(TopicArn=topic_id,Protocol='lambda',Endpoint=function_arn)
    lambda_client.add_permission(FunctionName=function_name,StatementId=user_id,Action="lambda:InvokeFunction",Principal="sns.amazonaws.com",SourceArn=topic_id)

def main():
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",action='store',dest="credentials_dir",default="/data/.aws",
                    help="credentials_dir, directory with AWS credentials")
    parser.add_argument("-t", action='store',dest="topic_name",default="dtoxspubsub",
                    help="topic_name, identifier for topic")
    parser.add_argument("--fn", action='store',dest="function_name",default="dtoxsfunction",
                    help="function_name, name of lambda function")
    parser.add_argument("--fr", action='store',dest="function_region",default="us-east-1",
                    help="function_region, region of lambda function")              
    parser.add_argument("--handler", action='store',dest="handler",default="main.lambda_handler",
                    help="handler, name of lambda function handler")
    parser.add_argument("-m", action='store',dest="memory",default=2048,
                    help="memory, lambda function RAM in MB")
    parser.add_argument("--timeout", action='store',dest="timeout",default=540,
                    help="timeout, maximum runtime of function before timing out")
    parser.add_argument("-p", action='store',dest="policy_name",default="dtoxspolicy",
                    help="policy_name, name of the aws policy")
    parser.add_argument("--role", action='store',dest="role_name",default="dtoxsrole",
                    help="role_name, name of the aws role")
    parser.add_argument("--fz", action='store',dest="function_zipfile",default="/data/dtoxsfunction.zip",
                    help="function_zipfile, name of the zipped function file")
    parser.add_argument("-u", action='store',dest="user_id",default="dtoxsuser",
                    help="user_id, user_id")
    args=parser.parse_args()
    
    credentials_dir=args.credentials_dir
    topic_name=args.topic_name
    function_name=args.function_name
    function_region=args.function_region
    handler=args.handler
    memory=int(args.memory)
    timeout=args.timeout
    policy_name=args.policy_name
    role_name=args.role_name
    function_zipfile=args.function_zipfile
    user_id=args.user_id

    
    print("credentials directory={}".format(credentials_dir))
#    print("bucket_name={}".format(bucket_name))
    print("topic_name={}".format(topic_name))
    print("function_name={}".format(function_name))
    print("function_region={}".format(function_region))
    print("handler={}".format(handler))
    print("memory={}".format(memory))
    print("timeout={}".format(timeout))
    print("policy_name={}".format(policy_name))
    print("role_name={}".format(role_name))
    print("function_zipfile={}".format(function_zipfile))
    print("user_id={}".format(user_id))

    #copy credentials
    execute('''cp -r %s/* /root/.aws/. '''%(credentials_dir))
    
    #initialize clients
    global sns_client,iam_client,lambda_client
    sns_client=boto3.client('sns',region_name=function_region)
    iam_client=boto3.client('iam',region_name=function_region)
    lambda_client=boto3.client('lambda',region_name=function_region)

    
    topic_id=create_topic(topic_name)
    sys.stderr.write("topic_id is {}\n".format(topic_id))
    deploy_function(topic_id,topic_name,function_name,function_zipfile,handler,memory,timeout,policy_name,role_name,user_id)


main()
