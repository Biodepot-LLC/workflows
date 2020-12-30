#!/bin/bash
if [ -z $reverse_order ]; then
 echo "bam-somaticsniper $@"
 bam-somaticsniper $@
else
 output="${@: -1}"
 set -- "${@:1:$(($#-1))}"
 tumor="${@: -1}"
 set -- "${@:1:$(($#-1))}"
 normal="${@: -1}"
 set -- "${@:1:$(($#-1))}"
  echo "bam-somaticsniper $@ $tumor $normal $output"
  bam-somaticsniper $@ $tumor $normal $output
fi
