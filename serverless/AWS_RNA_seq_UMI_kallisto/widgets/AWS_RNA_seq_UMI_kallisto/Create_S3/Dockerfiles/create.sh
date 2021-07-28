#!/bin/bash

awsdir=$1
bucket=$2
region=$3


#copy credentials
cp -r $awsdir/* /root/.aws || exit 1
#create bucket if necessary
aws s3api  head-bucket --bucket $bucket --region $region &>/dev/null && echo "bucket exists" || aws s3api create-bucket --bucket $bucket --region $region --create-bucket-configuration LocationConstraint=$region

