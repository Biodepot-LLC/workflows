#!/bin/bash
#will do a directory based recursive upload - the file level parallelism will not work well with low bandwidths esp on servers that are not EC2
awsdir=$1
DIR=$2
bucket=$3
glob=$4

#copy credentials
if [ -d "$awsdir" ]; then
	cp -r $awsdir/* /root/.aws || exit 1
else
	# Check if IAM role is attached if credentials do not exist
	aws sts get-caller-identity || exit 1
fi

#with one thread just copy the directory
if [ -z ${NTHREADS} ]; then
	aws s3 cp $DIR s3://$bucket/$glob --recursive
	exit $?
fi

runJob(){
	lasti=$((${#DIRS[@]} - 1))
	for i in $(seq 0 ${lasti}); do
		if (mkdir $lockDir/lock$i 2> /dev/null ); then
			d=${DIRS[$i]}
			echo thread $1 working on $d
			cmd="cd $DIR && nice aws s3 cp $d s3://$bucket/$glob/$d --recursive"
			exec $cmd
		fi
	done
	exit
}

DIRS=( $(cd $DIR && find * -maxdepth 0 -type d) )
#if there are directories
if (( ${#DIRS[@]} )); then
	lockDir=/tmp/locks.$$
	mkdir -p $lockDir
	for i in $(seq 2 $NTHREADS); do
		runJob $i &
	done
	runJob 1 &
	wait
	rm -rf $lockDir
else
	aws s3 cp $DIR s3://$bucket/$glob --recursive
	exit $?
fi
