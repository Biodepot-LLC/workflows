#!/bin/bash
printenv
if [ -z "$OUTPUTDIR" ]; then
   exit 1
fi
rm ${OUTPUTDIR}/*.done -f
rm ${OUTPUTDIR}/*/* -f
rm ${OUTPUTDIR}"_done" -rf
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
       if [ -z ${nobarcode+x} ]; then
		echo "$NWELLS/umisplit $parms $R1File $R2File &> $logFile &"
		$NWELLS/umisplit -o $OUTPUTDIR $parms $R1File $R2File &> $logFile &
	   else
		echo "$NWELLS/umisplit_pe -o $OUTPUTDIR $parms $R1File $R2File &> $logFile &"
		$NWELLS/split_pe -o $OUTPUTDIR $parms $R1File $R2File &> $logFile &	   
	   fi
     fi
   fi
 done
}
launchSEfiles(){
 for fastqFile in ${fastqFiles[@]}; do
   if [[  -z ${fastqSeen[$fastqFile]} ]]; then
     fastqSeen[$fastqFile]=1
     logFile=fastqFile".log" 
	 echo "$NWELLS/split_se -o $OUTPUTDIR $parms $fastqFile &> $logFile &"
	 $NWELLS/split_se -o $OUTPUTDIR $parms $fastqFile &> $logFile &
   fi
 done
}
date
declare -A R1Files
declare -A R2Files
declare -A pairSeen
declare -A fastqSeen

#should add a check here to see if the maximum number of threads is being used before launching new jobs
while [ 1 ]; do
 echo "find $SEQS_DIR -name *.${fastq_suffix}"
 fastqFiles=( $( find $SEQS_DIR -name *.${fastq_suffix} ) )
 if [ -z ${nobarcode+x} ] || (( $npairs > 0 )); then
  echo "$npairs splitting files"
   splitR1R2Pairs
   npairs_launched="${#pairSeen[@]}"
   if (( npairs_launched >= npairs )); then
     echo "All $npairs pairs begun splitting $(date)"
     break
   fi
 else
   echo "launching files"
   launchSEfiles
   nfiles_launched="${#fastqSeen[@]}"
   if (( nfiles_launched >= nfiles )); then
     echo "All $nfiles fastq begun splitting $(date)"
     break
   fi
 fi
 sleep 1
done
echo "waiting on $upload_pid"
wait $upload_pid

