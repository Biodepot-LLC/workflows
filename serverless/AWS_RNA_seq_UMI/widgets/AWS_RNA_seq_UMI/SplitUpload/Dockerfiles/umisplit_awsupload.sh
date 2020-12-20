#!/bin/bash

printenv
if [ -z "$OUTPUTDIR" ]; then
   exit 1
fi
rm ${OUTPUTDIR}/*.done
rm ${OUTPUTDIR}/*/*
rm ${OUTPUTDIR}"_done" -r
mkdir -p ${OUTPUTDIR}
cp -r $awsdir/* /root/.aws
parms=$@
echo "nice runUploadSplitFiles.sh $OUTPUTDIR $NFILES s3://${BUCKET}/${CLOUD_DIR} $UPLOAD_THREADS $UPLOAD_THREADS_AFTER &"
nice runUploadSplitFiles.sh $OUTPUTDIR $NFILES s3://${BUCKET}/${CLOUD_DIR} $UPLOAD_THREADS $UPLOAD_THREADS_AFTER &
upload_pid=$!

npairs_launched=0
splitR1R2Pairs(){
 for fastqFile in ${fastqFiles[@]}; do
   fastqbase=${fastqFile##*/}
   if [[ $fastqbase == *"${R1fastq_suffix}"* ]]; then
     R1Files[$fastqFile]=1
   elif [[ $fastqbase == *"${R2fastq_suffix}"* ]]; then
     R2Files[$fastqFile]=1
   fi
 done
 for fastqFile in "${!R1Files[@]}"; do
   echo "$fastqFile"
   if [[  -z ${pairSeen[$fastqFile]} ]]; then
     fastqbase=${fastqFile##*/}
     filebase="${fastqbase%${R1fastq_suffix}}"
     fileExt="${fastqbase#*.}"
     echo "$fastqbase $filebase $fileExt"
     R2fastqFile="$SEQS_DIR/$filebase""$R2fastq_suffix"    
     logFile="$OUTPUTDIR/$filebase""R1R2.log"
     if [[ ${R2Files[$R2fastqFile]+1}  ]]; then
       pairSeen[$fastqFile]=1
       R1File=$fastqFile
       R2File=$R2fastqFile
       echo "$NWELLS/umisplit $parms $R1File $R2File &> $logFile &"
       $NWELLS/umisplit $parms $R1File $R2File &> $logFile &
     fi
   fi
 done
}
date
declare -A R1Files
declare -A R2Files
declare -A pairSeen


while [ 1 ]; do
 echo "find $SEQS_DIR -name *.${fastq_suffix}"
 fastqFiles=( $( find $SEQS_DIR -name *.${fastq_suffix} ) )
 splitR1R2Pairs
 npairs_launched="${#pairSeen[@]}"
 if ((npairs_launched>=npairs)); then
  echo "All $npairs pairs begun splitting $(date)"
  break
 fi
 sleep 1
done
echo "waiting on $upload_pid"
wait $upload_pid

