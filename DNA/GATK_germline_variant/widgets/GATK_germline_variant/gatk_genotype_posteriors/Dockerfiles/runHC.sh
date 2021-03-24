#!/bin/bash

echo "gatk --java-options \"-Xmx4g\" HaplotypeCaller $@"
gatk --java-options "-Xmx4g" HaplotypeCaller $@
