#!/bin/bash
if [[ -n "$bypass" &&
	-s "$genomeDir/SA" &&
	-s "$genomeDir/Genome" &&
	-s "$genomeDir/SAindex" &&
	-s "$genomeDir/exonGeTrInfo.tab" &&
	-s "$genomeDir/exonInfo.tab" &&
	-s "$genomeDir/transcriptInfo.tab" &&
	-s "$genomeDir/sjdbList.fromGTF.out.tab" &&
	-s "$genomeDir/sjdbInfo.txt" &&
	-s "$genomeDir/sjdbList.out.tab" &&
	-s "$genomeDir/geneInfo.tab" &&
	-s "$genomeDir/chrNameLength.txt" &&
	-s "$genomeDir/chrStart.txt" &&
	-s "$genomeDir/chrName.txt" &&
	-s "$genomeDir/genomeParameters.txt" &&
	-s "$genomeDir/chrLength.txt" ]]
then
	echo "bypassing STAR generate index"
else
	STAR "$@"
fi
