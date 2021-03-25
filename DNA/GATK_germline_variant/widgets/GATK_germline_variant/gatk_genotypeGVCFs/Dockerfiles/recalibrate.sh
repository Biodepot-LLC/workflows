#!/bin/bash

bqsrfile=${outputfile%.*}_bqsr.table

echo "gatk BaseRecalibrator --known-sites $snps $@ -O $bqsrfile"
gatk BaseRecalibrator --known-sites $snps $@ -O $bqsrfile
echo "gatk ApplyBQSR --bqsr-recal-file $bqsrfile $@ -O $outputfile"
gatk ApplyBQSR --bqsr-recal-file $bqsrfile $@ -O $outputfile

