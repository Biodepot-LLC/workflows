#!/bin/bash
if [ -n "$bypass" ]; then
	echo "bypassing STAR generate index"
else
	STAR "$@"
fi
