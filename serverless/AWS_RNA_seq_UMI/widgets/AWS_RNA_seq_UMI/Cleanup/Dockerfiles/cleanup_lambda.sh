#!/bin/bash
env
cp -r $AWSDIR/* /root/.aws/.
function ask_yes_or_no() {
    read -p "$1 ([y]es or [N]o): "
    case $(echo $REPLY | tr '[A-Z]' '[a-z]') in
        y|yes) echo "yes" ;;
        *)     echo "no" ;;
    esac
}
if [[ $DELETE_ROLE ]]; then
	echo "deleting role"
	echo "aws iam delete-role-policy --role-name $ROLE_NAME --policy-name $POLICY_NAME"
	aws iam delete-role-policy --role-name $ROLE_NAME --policy-name $POLICY_NAME
	echo "aws iam delete-role --role-name $ROLE_NAME"
	aws iam delete-role --role-name $ROLE_NAME || ERROR=true
fi

if [[ $DELETE_FUNCTION ]]; then
	echo "deleting lambda function"
	echo "aws lambda delete-function --region $FUNCTION_REGION --function-name $FUNCTION_NAME"
	aws lambda delete-function --region $FUNCTION_REGION --function-name $FUNCTION_NAME || ERROR=true
fi

if [[ $DELETE_QUEUE ]]; then
    echo "$SUBSCRIPTION_NAME $FUNCTION_REGION| $RTOPIC $TOPIC"
	echo "deleting queue and topics"
	echo "deleting topics"
    echo "aws sns delete-topic --topic-arn $RTOPIC"
    #need to create topic to find the arn from the name - then delete it
    RTOPIC_ARN=$( aws sns create-topic --name $RTOPIC | jq -r '."TopicArn"' )
    echo "aws sns delete-topic --topic-arn $RTOPIC_ARN"
    aws sns delete-topic --topic-arn $RTOPIC_ARN || ERROR=true
    TOPIC_ARN=$( aws sns create-topic --name $TOPIC | jq -r '."TopicArn"' )
    echo "aws sns delete-topic --topic-arn RTOPIC_ARN"
    aws sns delete-topic --topic-arn $TOPIC_ARN || ERROR=true
    echo "obtaining queue url" 
	qurl=$( aws sqs get-queue-url --queue-name $SUBSCRIPTION_NAME --region $FUNCTION_REGION| jq -r '."QueueUrl"' )
	echo "queue url is $qurl"
	echo "deleting queue"
	echo "aws sqs delete-queue --region $FUNCTION_REGION --queue-url $qurl"
	#looks like it actually deletes it and then returns an error when it can't find it any more
	aws sqs delete-queue --region $FUNCTION_REGION --queue-url $qurl
fi
if [[ $DELETE_ALIGN_FILES ]]; then
   echo "deleting alignment results on S3"
   echo "aws s3 rm s3://$BUCKET_NAME/$WORK_DIR/start --recursive" 
   aws s3 rm "s3://$BUCKET_NAME/$WORK_DIR/start" --recursive  || ERROR=true
   echo "aws s3 rm s3://$BUCKET_NAME/$WORK_DIR/saf --recursive" 
   aws s3 rm "s3://$BUCKET_NAME/$WORK_DIR/saf" --recursive  || ERROR=true
   echo "rm -rf $LOCAL_WORK_DIR/saf"
   rm -rf $LOCAL_WORK_DIR/saf
   rm -rf $LOCAL_WORK_DIR/Counts/*.dat
   rm -rf $LOCAL_WORK_DIR/Results/FDR*

fi

if [[ $DELETE_SPLIT_FILES ]]; then
	echo "deleting split files on S3"
	echo "aws s3 rm s3://$BUCKET_NAME/$CLOUD_SPLIT_DIR --recursive"
	aws s3 rm s3://$BUCKET_NAME/$CLOUD_SPLIT_DIR --recursive || ERROR=true
fi

if [[ $DELETE_CLOUD_FILES ]]; then
	echo "deleting all project files on S3"
	echo "aws s3 rm s3://$BUCKET_NAME/$WORK_DIR --recursive" 
    aws s3 rm "s3://$BUCKET_NAME/$WORK_DIR" --recursive  || ERROR=true
fi

if [[ $DELETE_BUCKET ]]; then
	echo "deleting S3 bucket"
	echo "aws s3api delete-bucket --bucket $BUCKET_NAME"
    aws s3api delete-bucket --bucket $BUCKET_NAME || ERROR=true
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
