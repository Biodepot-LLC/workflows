#!/bin/bash 
 if [ -z ${prefix+x} ]; then
	baseFile=$reference
 else
    baseFile=$prefix
 fi  

 { [ -f ${baseFile}.64.bwt ] || [ -f ${baseFile}.bwt ]; } && [ -z ${overwrite+x} ] && echo "reference exists and will not overwrite" && exit 0 
  echo "bwa index $@"
  bwa index $@ 
  #cannot trust return code on this from github issue - if the SA file is constructed then it probably is OK
  { [ -f ${baseFile}.64.sa ] || [ -f ${baseFile}.sa ]; }  && exit 0
  
