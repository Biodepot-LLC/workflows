#!/bin/bash

printenv

mkdir -p $work_dir || exit 1
mkdir -p $genome_dir || exit 1
# Variant Effect Predictor (DNA seq workflow) needs permissions set for UID 999
if [ -n "$vep_dir" ]; then
	mkdir -p $vep_dir || exit 1
	chown 999 $vep_dir
fi
