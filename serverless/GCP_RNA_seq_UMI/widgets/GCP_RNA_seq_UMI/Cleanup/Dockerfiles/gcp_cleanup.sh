#!/bin/bash

function deleteSub () {
	topic=$1
	subs=($(gcloud pubsub topics list-subscriptions ${topic} | sed -e 's/---//' | sed -e 's/^[ \t\n\r]*//'))
	for sub in ${subs[@]}; do
		echo "gcloud pubsub subscriptions delete $sub"
		gcloud pubsub subscriptions delete $sub
	done
}

confirmationFile=$1
project_id=$(jq -r '.project_id' $confirmationFile)
gcloud config set project $project_id
echo "gcloud auth activate-service-account --key-file=$confirmationFile"
gcloud auth activate-service-account --key-file=$confirmationFile

if [[ $DELETE_FUNCTION ]]; then
	echo "deleting function $FUNCTION_NAME"
	gcloud functions delete --quiet $FUNCTION_NAME || echo "unable to delete $FUNCTION_NAME"
fi
if [[ $DELETE_QUEUE ]]; then
	echo "deleting pubsub subscriptions topics $TOPIC $RTOPIC"
	deleteSub $TOPIC
	deleteSub $RTOPIC
	echo "deleting pubsub topics"
	gcloud pubsub topics delete $TOPIC || echo "unable to delete $TOPIC "
	gcloud pubsub topics delete $RTOPIC  || echo "unable to delete $RTOPIC "
	
fi
if [[ $DELETE_ALIGN ]]; then
   echo "deleting cloud alignment results"
   echo "gsutil -m rm -r gs://$BUCKET_NAME/$WORK_DIR/start"
   gsutil -m rm -r gs://$BUCKET_NAME/$WORK_DIR/start
   echo "gsutil -m rm -r gs://$BUCKET_NAME/$WORK_DIR/saf"
   gsutil -m rm -r gs://$BUCKET_NAME/$WORK_DIR/saf
   echo  "deleting local alignment files"
   rm -rf $LOCAL_WORK_DIR/saf
   rm -rf $LOCAL_WORK_DIR/Counts/*.dat
   rm -rf $LOCAL_WORK_DIR/Results/FDR*
fi
if [[ $DELETE_SPLIT ]]; then
   echo "deleting cloud split files"
   echo "gsutil -m rm -r gs://$BUCKET_NAME/$CLOUD_SPLIT_DIR"
   gsutil -m rm -r gs://$BUCKET_NAME/$CLOUD_SPLIT_DIR || ERROR=true
fi
if [[ $DELETE_CLOUD_FILES ]]; then
   echo "deleting cloud project files"
   echo "gsutil -m rm -r gs://$BUCKET_NAME/$WORK_DIR "
   gsutil -m rm -r gs://$BUCKET_NAME/$WORK_DIR || ERROR=true
fi

if [[ $DELETE_BUCKET ]]; then
	echo "deleting bucket $BUCKET_NAME"
	gsutil -m rm -r gs://$BUCKET_NAME || ERROR=true
fi	
if [[ $DELETE_LOCAL ]]; then
	echo "deleting local files"
	if [[ -z $LOCAL_WORK_DIR ]]; then
	   echo "no local working directory defined"
	   ERROR=true
	else
	   echo "rm -rf $LOCAL_WORK_DIR"
	   rm -rf $LOCAL_WORK_DIR
	fi
fi

if [ "$ERROR" = true ]; then
	exit 1
fi
