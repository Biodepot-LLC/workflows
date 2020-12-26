#!/bin/bash

confirmationFile=$1
bucket=$2
function_name=$3
function_dir=$4
entrypoint=$5
runtime=$6 #python37
topic_id=$7
timeout=$8
memory=$9
max_instances=${10}
region=${11}

if (( memory < 192 )); then
	memory='128MB'
elif (( memory < 384 )); then
	memory='256MB'
elif (( memory < 768 )); then
	memory='512MB'
elif (( memory < 1536 )); then
	memory='1024MB'
else
	memory='2048MB'
fi

project_id=$(jq -r '.project_id' $confirmationFile)
gcloud config set project $project_id
echo "gcloud auth activate-service-account --key-file=$confirmationFile"
gcloud auth activate-service-account --key-file=$confirmationFile

echo "gcloud services enable cloudresourcemanager.googleapis.com"
gcloud services enable cloudresourcemanager.googleapis.com

echo "gcloud functions deploy $function_name --region=$region --entry-point $entrypoint --memory $memory --runtime $runtime --source $function_dir --timeout $timeout --trigger-topic $topic_id --max-instances $max_instances --allow-unauthenticated "
gcloud functions deploy $function_name --region=$region --entry-point $entrypoint --memory $memory --runtime $runtime --source $function_dir --timeout $timeout --trigger-topic $topic_id --max-instances $max_instances --allow-unauthenticated
