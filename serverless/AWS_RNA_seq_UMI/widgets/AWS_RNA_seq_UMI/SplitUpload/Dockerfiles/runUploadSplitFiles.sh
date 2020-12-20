#!/bin/bash
ALIGNS_DIR=$1
nseq=$2
cloudPath=$3
#Threads before split is done
NTHREADS1=$4
#Threads after split is done
NTHREADS2=$5
done_dir=$ALIGNS_DIR"_done"
mkdir -p $done_dir
while [ 1 ]; do
 ndone=`ls ${ALIGNS_DIR}/*.done | wc -l`
 if [ "${nseq}" == "${ndone}" ]; then
    uploadSplitFiles.sh $ALIGNS_DIR $cloudPath $done_dir $NTHREADS2
    exit 0
 fi
 uploadSplitFiles.sh $ALIGNS_DIR $cloudPath $done_dir $NTHREADS1
 sleep 1
done
rm $done_dir -r
