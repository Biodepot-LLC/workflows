#!/bin/bash

# Required arguments
base=${input%.*}
output="$base""$output_suffix"
metrics="$base""$metrics_suffix"

# Constructing command and appending optional arguments
cmd="gatk MarkDuplicates --INPUT $input --OUTPUT $output --METRICS_FILE $metrics $@"

# Executing command
echo "$cmd"
$cmd

# Return status
exit $?
