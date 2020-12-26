#!/bin/bash
confirmationFile=$1
ALIGNS_DIR=$2
nseq=$3
cloudPath=$4
#Threads before split is done
NTHREADS1=$5
#Threads after split is done
NTHREADS2=$6
done_dir=$ALIGNS_DIR"_done"
project_id=$(jq -r '.project_id' $confirmationFile)
gcloud config set project $project_id
echo "gcloud auth activate-service-account --key-file=$confirmationFile"
gcloud auth activate-service-account --key-file=$confirmationFile
while [ 1 ]; do
 ndone=`ls ${ALIGNS_DIR}/*.done | wc -l`
 if [ "${nseq}" == "${ndone}" ]; then
    echo "found all $ndone of $nseq files"
    nice uploadSplitFiles.sh $ALIGNS_DIR $cloudPath $done_dir $NTHREADS2
    exit 0
 fi
 echo "only found $ndone of $nseq files"
 nice uploadSplitFiles.sh  $ALIGNS_DIR $cloudPath $done_dir $NTHREADS1
 sleep 1
done
rm -r $done_dir
