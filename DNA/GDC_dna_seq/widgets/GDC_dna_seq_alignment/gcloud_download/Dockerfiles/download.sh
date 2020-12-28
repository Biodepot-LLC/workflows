#!/bin/bash

bucket=$1
outputDir=$2

gsutil -q ls gs://${bucket}/ &>/dev/null
 
if [ $? != 0 ]; then
	echo "cannot find cloud directory ${bucket}"
	exit -1
fi

mkdir -p $outputDir

if [ -z $DIRS ]; then
	echo "no directories to download"
elif [ "$DIRS" == "[]" ]; then
	if [[ $(gsutil ls gs://${bucket}) ]]; then
		echo "downloading the entire bucket $bucket"
		echo "gsutil -m cp -r gs://${bucket}/* $outputDir/."
		gsutil -m cp -r gs://${bucket}/* $outputDir/.
	fi
else
	darray=( $(echo $DIRS | jq -r '.[]') )
	if [ -z $darray ]; then
		echo "cannot parse $DIRS"
	else
		for dir in "${darray[@]}"; do
			gsutil -q ls gs://${bucket}/${dir} &>/dev/null
			if [ $? == 0 ]; then
				if [[ $(gsutil ls gs://${bucket}/${dir}) ]]; then
					echo "downloading ${bucket}/${dir}"
					echo "gsutil -m cp -r gs://${bucket}/${dir}/* $outputDir/."
					gsutil -m cp -r gs://${bucket}/${dir}/* $outputDir/.
				fi
			else
				echo "cannot find or cannot access ${bucket}/${dir}"
			fi
		done
	fi
fi
if [ -z $FILES ]; then
	echo "no files to download"
else
	echo $FILES
	farray=( $(echo $FILES | jq -r '.[]') )
	for f in "${farray[@]}"; do
		gsutil -q ls gs://${bucket}/${f} &>/dev/null
		if [ $? == 0 ]; then
			echo "downloading ${bucket}/${f}"
			echo "gsutil -m cp gs://${bucket}/${f} $outputDir/."
			gsutil -m cp gs://${bucket}/${f} $outputDir/.
		else
			echo "cannot find or cannot access ${bucket}/${f}"
		fi
	done
fi
