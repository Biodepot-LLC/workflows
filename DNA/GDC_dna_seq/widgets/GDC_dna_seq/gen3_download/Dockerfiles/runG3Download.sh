#!/bin/bash

#things to do - can obtain manifest from endpoint for any guid to get file and md5 hash so we can verify before proceeding

gdcapiurl='https://api.gdc.cancer.gov'
exitCode=0

#create a temporary directory for API download and mv the downloads when complete an no error
#remove the temporary directory if there is a interrupt or error
#if there is an error save the uid for download using gen3
#need to also check for gen3 errors

function cleanup(){
	#use global tempDir as this will depend on the GUID being downloaded or the manifest being downloaded
	#make sure that basename tempdir starts with temp so that we don't remove something disastrous with a typo
	basetemp=$(basename $tempDir)
	[[ -n "$basetemp" && "${basetemp:0:4}" = "temp" ]] && rm -rf $tempDir
}

#call cleanup if we exit not so nicely
trap "cleanup  -1 " SIGINT INT TERM

#there is a bug with the multi-download api in that the files are not properly tarballed - so use only singleDownload endpoint
function singleDownloadGET(){
	local myid=$1
	local downloaded=0
	tempDir=$(mktemp -d -p $downloadDir -t tempXXXXXX)
	if [ -z "$tempDir" ]; then
		echo "ERROR: failed to create temp directory to store download"
		return $downloaded
	fi
	pushd $tempDir > /dev/null
	if ! curl -OJ --header "X-Auth-Token: $token" $gdcapiurl/data/$myid; then
		echo "curl error $?"
	elif [ -f "$tempDir/$myid" ]; then
		cat $tempDir/$myid
	elif [ -f "$tempDir/data" ]; then
		cat $tempDir/data
	elif [ -n "$(ls -A $tempDir/*tar)" ]; then
		# download successful
		if [[ -n "$untarfiles" && "$untarfiles" = "True" ]]; then
			tar -xf $tempDir/* -C $downloadDir
		else
			mv $tempDir/* $downloadDir
		fi
		downloaded=1
	fi
	popd > /dev/null
	cleanup
	return $downloaded
}

function convertManifest(){
	echo "tail -n +2 $manifest | awk '{printf "%s ",$1}'"
	guidsArray=($(tail -n +2 $manifest | awk '{printf "%s ",$1}'))
}

function downloadWithToken(){
	if [ -n "$manifest" ]; then
		convertManifest
	else
		guidsArray=($(convertJsonToArrayNoQuotes $guids))
	fi
	local myArray=()
	for guid in "${guidsArray[@]}"; do
		singleDownloadGET $guid && myArray+=($guid)
	done
	guidsArray=(${myArray[@]})
	return ${#myArray[@]}
}

function convertJsonToArrayNoQuotes(){
	#echos out a string that can be converted to a bash array to get around not being able to return string or array
	local string=$1
	if [ ${string:0:1} = '[' ];then
		#remove square brackets at beginning and end with substring
		#put spaces with , replacement
		#remove all " in this case
		string=$(echo "${string:1:${#string}-2}" | sed 's/\,/ /g' | sed 's/\"/ /g')
	fi
	echo "$string"
}

function singleDownload(){
	[ -z $guidsArray ] && guidsArray=($(convertJsonToArrayNoQuotes $guids))
	for guid in "${guidsArray[@]}"; do
		local cmd="gen3-client download-single --profile=$profile --no-prompt --guid=$guid ${flags[@]}"
		local log="/tmp/log$guid"
		echo $cmd
		$cmd 2> >(tee -a $log >&2)
		errors=$(fgrep 'Details of error:' $log)
		if [ -n "$errors" ]; then
			echo "Exiting with error $errors"
			exitCode=1
			return
		fi
	done
}

function multiDownload(){
	echo "Downloading using manifest"
	local cmd="gen3-client download-multiple --profile=$profile --no-prompt ${flags[@]}"
	local log="/tmp/logManifest"
	echo $cmd
	$cmd 2> >(tee -a $log >&2)
	errors=$(fgrep 'Details of error:' $log)
	if [ -n "$errors" ]; then
		echo "Exiting with error $errors"
		exitCode=1
	fi
}

#check if both guid and manifest given
#For now force user to use one or the other - otherwise this may cause difficulties with auto-multithread with the manifest being downloaded each time
#they can use two instances of the widget if they really want to do this and not merge the manifest
#if we pass a flag to indicate multi-thread execution (which we may) then we might modify this
if [[ -n $guids && -n $manifest ]]; then
	echo "Please choose either a GUID or a manifest file not both"
	echo "You can merge the GUID into the manifest or use two instances of the widget to download both"
	exit 1
fi

#First try with the old api
if [[ -n "$gdctoken" && -f "$gdctoken" ]]; then
	token=$(cat $gdctoken)
	#if there are no files left in guidsArray then all files have been successfully downloaded - exit
	downloadWithToken && exit 0
fi

echo "no gdc token given - use gen3 fence to download"
echo "Attempting to authenticate using gen3 fence service"
#Authenticate the container by copying or creating a config
#the commons might change so we do not hardcode the url
[ -z $datacommons_url ] && datacommons_url="https://nci-crdc.datacommons.io/"

#assume config file basename is config when given by user
#otherwise assume that the file given by user is a credentials file
credBasename=$(basename $cred)
if [ $credBasename == "config" ]; then
	mkdir -p /root/.gen3
	cp $cred /root/.gen3/config
elif ! gen3-client configure --profile=$profile --cred=$cred --apiendpoint=$datacommons_url; then
	echo "was not successful in creating new profile"
	exit 1
fi

#check if we have a configuration defined now
if [ -f "/root/.gen3/config" ]; then
	#now we can begin download
	flags=( "$@" )
	gen3-client auth --profile=$profile
	if [ -z $manifest ]; then
		singleDownload
	else
		multiDownload
	fi
else
	echo "must provide a valid config or credentials file"
	exit 1
fi

exit $exitCode
