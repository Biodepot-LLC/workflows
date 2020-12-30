#!/bin/bash
if [ -z $reverse_order ]; then
 echo "muse call $@"
 muse call $@
else
 tumor="${@: -1}"
 set -- "${@:1:$(($#-1))}"
 normal="${@: -1}"
 set -- "${@:1:$(($#-1))}"
  echo "muse call $@ $tumor $normal"
 muse call $@ $tumor $normal
fi
