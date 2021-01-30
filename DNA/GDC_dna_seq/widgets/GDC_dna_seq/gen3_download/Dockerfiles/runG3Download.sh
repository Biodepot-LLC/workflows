#!/bin/bash

#things to do - can obtain manifest from endpoint for any guid to get file and md5 hash so we can verify before proceeding

gdcapiurl='https://api.gdc.cancer.gov'

#create a temporary directory for API download and mv the downloads when complete an no error
#remove the temporary directory if there is a interrupt or error
#if there is an error save the uid for download using gen3
#need to also check for gen3 errors

function cleanup(){
 #use global tempDir as this will depend on the GUID being downloaded or the manifest being downloaded
 #make sure that basename tempdir starts with temp so that we don't remove something disastrous with a typo
 basetemp=$(basename tempDir) 
 if [ ${basetemp:0:4} == 'temp' ]; then
	rm -rf $tempDir
 fi
}

#call cleanup if we exit not so nicely
trap "cleanup  -1 " SIGINT INT TERM

#there is a bug with the multi-download api in that the files are not properly tarballed - so use only singleDownload endpoint
function singleDownloadGET(){
 local myid=$1
 downloaded=0
 cd $tempDir; curl -OJ --header "X-Auth-Token: $token" $gdcapiurl/data/$myid
 if [[ $? != 0 ]]; then
   echo "curl error $?"
   cleanup
   return
 else
   if [ -f "$tempDir/$guid" ]; then
     cat $tempDir/$guid
     cleanup
     return
   fi
   if [ -f "$tempDir/$data" ]; then
     cat $tempDir/data
     cleanup
     return
   fi  
   if [ -z "$(ls -A $tempDir)" ]; then
     cleanup
     return
   fi
   mv $tempDir/* $outputDir/
   downloaded=1
   cleanup
   return     
 fi
}
function convertManifest(){
 echo "tail -n +2 $manifest | awk '{printf "%s ",$1}'"
 guidsArray=($(tail -n +2 $manifest | awk '{printf "%s ",$1}'))
}

function downloadWithToken(){
  if [ -n $manifest ]; then
    convertManifest
  else
    guidsArray=($(convertJsonToArrayNoQuotes $guids))
  fi
  myArray=()
  for guid in "${guidsArray[@]}"; do
    tempDir=$outputDir/temp$guid
    mkdir -p $tempDir
    singleDownloadGET $guid
    if [ $downloaded == 0 ];then
      myArray+=($guid)  
    fi
  done
  guidsArray=(${myArray[@]})
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
 if [ -z $guidsArray ]; then
   guidsArray=($(convertJsonToArrayNoQuotes $guids))
 fi
 for guid in "${guidsArray[@]}"; do
   echo "gen3-client download-single --profile=$profile --no-prompt --guid=$guid ${flags[@]}"
   gen3-client download-single --profile=$profile --no-prompt --guid=$guid ${flags[@]} 
 done
}
function multiDownload(){
  echo "Downloading using manifest"	
  echo "gen3-client download-multiple --profile=$profile --no-prompt ${flags[@]}"
  gen3-client download-multiple --profile=$profile --no-prompt ${flags[@]} 
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
if [ -n $gdctoken ]; then
  if [ -f $gdctoken ]; then
    token=$(cat $gdctoken)
    downloadWithToken
    exit
    if [ $? == 0 ]; then
      exit 0
    else
      echo "Unable to download using gdc token"
    fi
  fi
  #if there are no files left in guidsArray then all files have been successfully downloaded - exit
  (( ${#guidsArray[@]} )) || exit 0 
fi

echo "Attempting to authenticate using gen3 fence service"
#Authenticate the container by copying or creating a config
#the commons might change so we do not hardcode the url
if [ -z $datacommons_url ]; then
	datacommons_url="https://nci-crdc.datacommons.io/"
fi

#assume config file basename is config when given by user
#otherwise assume that the file given by user is a credentials file

credBasename=$(basename $cred)
if [ $credBasename == "config" ]; then
    mkdir -p /root/.gen3
   	cp credBasename /root/.gen3/config
else
  gen3-client configure --profile=$profile --cred=$cred --apiendpoint=$datacommons_url
  if [ $? != 0 ]; then
    echo "was not successful in creating new profile"
    exit 1
  fi
fi

#check if we have a configuration defined now
if [ -f "/root/.gen3/config" ]; then
 #now we can begin download
 flags=( "$@" ) 
 gen3-client auth --profile=$profile
 if [ -n $manifest ]; then 
	multiDownload
 else
    singleDownload
 fi
else
  echo "must provide a valid config or credentials file" 
  exit 1 
fi


