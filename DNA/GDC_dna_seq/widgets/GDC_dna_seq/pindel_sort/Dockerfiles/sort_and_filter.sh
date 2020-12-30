#!/bin/bash

echo "java -d64  -Xmx16G -jar picard.jar SortVcf CREATE_INDEX=true SEQUENCE_DICTIONARY=$dictionary I=$input OUTPUT=$output"

java -d64  -Xmx16G -jar picard.jar SortVcf CREATE_INDEX=true SEQUENCE_DICTIONARY=$dictionary I=$input OUTPUT=$output

java -Xmx4G -jar /usr/GenomeAnalysisTK.jar -T VariantFiltration --disable_auto_index_creation_and_locking_when_reading_rods -V $output -R $reference --filterExpression "vc.isBiallelic() && vc.getGenotype(\"TUMOR\").getAD().1 < 3" --filterName TALTDP -o $outputfilter
