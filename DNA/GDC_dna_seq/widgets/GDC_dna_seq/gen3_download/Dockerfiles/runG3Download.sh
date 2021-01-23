#!/bin/bash

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
 guidsArray=($(convertJsonToArrayNoQuotes $guids))
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

#Authenticate the container by copying or creating a config
#the commons might change so we do not hardcode the url
if [ -z $api_endpoint_url ]; then
	api_endpoint_url="https://nci-crdc.datacommons.io/"
fi

#assume config file basename is config when given by user
#otherwise assume that the file given by user is a credentials file

credBasename=$(basename $cred)
if [ $credBasename == "config" ]; then
    mkdir -p /root/.gen3
   	cp credBasename /root/.gen3/config
else
  gen3-client configure --profile=$profile --cred=$cred --apiendpoint=$api_endpoint_url
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
 if [ -n $guids ]; then 
	singleDownload
 else
    multiDownload
 fi
else
  echo "must provide a valid config or credentials file" 
  exit 1 
fi


