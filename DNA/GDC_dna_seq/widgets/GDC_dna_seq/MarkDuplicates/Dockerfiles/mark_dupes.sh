
#!/bin/bash
input=$1
base=${input%.*}
output="$base""$2"
if [ -z $metrics_suffix ]; then
  echo "gatk MarkDuplicates --CREATE_INDEX true --INPUT $input --OUTPUT $output"
  gatk MarkDuplicates --CREATE_INDEX true --INPUT $input --OUTPUT $output
else
 metrics="$base""$metrics_suffix"
 echo "gatk MarkDuplicates --CREATE_INDEX true --INPUT $input --OUTPUT $output --METRICS_FILE $metrics"
 gatk MarkDuplicates --CREATE_INDEX true --INPUT $input --OUTPUT $output --METRICS_FILE $metrics
fi
