#!/bin/bash
#will look at all the files in the ALIGN DIR
ALIGN_DIR=$1
S3Path=$2
done_dir=$3
nThreads=$4




copyDirJobs(){
 lasti=$((${#dirs[@]} - 1))
 for i in $(seq 0 ${lasti}); do
  if (mkdir $lockDir/lock$i 2> /dev/null ); then
   dir=${dirs[i]}
   echo "cd $complete_dir && aws s3 cp $dir $S3Path/$dir --recursive"
   cd $complete_dir && aws s3 cp $dir $S3Path/$dir --recursive
  fi
 done
}
copyDirs(){
 dirs=( $(cd $complete_dir && find * -maxdepth 0 ! -empty -type d) )
 if (( ${#dirs[@]} )); then
   for i in $(seq 2 $nThreads); do
	  copyDirJobs $i &
   done
 fi
 copyDirJobs 1 &
 wait
}


#check if split is done
makeSubDirs(){
 subDirs=( $(cd $ALIGN_DIR && find * -type d) )
 for subDir in "${subDirs[@]}"
 do
	mkdir -p "$complete_dir/$subDir"
 done
}
move_complete(){
	for fileDone in "${files[@]}"
	do	
		file=${fileDone:2:(-5)}
		echo "cd $ALIGN_DIR && mv $file $complete_dir/$file && mv $fileDone $done_dir/."
	    cd $ALIGN_DIR && mv $file $complete_dir/$file && mv $fileDone $done_dir/. 
	done
}

files=( $(cd $ALIGN_DIR && find . -mindepth 2 -name '*.done') )
echo found "${#files[@]}" files

if (( ${#files[@]} )); then
	lockDir=/tmp/locks.$$
    complete_dir=$ALIGN_DIR"_complete".$(date "+%Y%m%d-%H%M%S")
	echo $complete_dir
	mkdir -p $lockDir
	makeSubDirs
	move_complete
	copyDirs
	echo "mv $complete_dir $done_dir/."
	mv $complete_dir $done_dir/.
	rm $lockDir -r
fi
