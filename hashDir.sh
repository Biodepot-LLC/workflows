#!/bin/bash
dir=$1
tarcmd=tar
if [ "$(uname)" == "Darwin" ]; then
    tarcmd=gtar
fi
if [ -z "$dir" ]; then
    echo "Usage: $0 <dir>"
    exit 1
fi
cmd="$tarcmd -C $dir -cf - --sort=name --portability  --mtime='UTC 2019-01-01' --group=0 --owner=0 --numeric-owner -T . | sha256sum"

#echo $cmd
eval $cmd | awk '{print $1}'