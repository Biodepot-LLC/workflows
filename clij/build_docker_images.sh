#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "WARNING: You are not root; you may not be permitted to access the Docker daemon, causing an error."
    echo "  If this occurs, re-run this script as root."
    echo ""
fi

WORKFLOW_NAME="clij_usability_demo"

function build_container () {
    WIDGET_NAME=$1
    DOCKER_IMAGE=$2
    DOCKER_TAG=$3

    pushd "`dirname $0`/$WORKFLOW_NAME/widgets/$WORKFLOW_NAME/$WIDGET_NAME/Dockerfiles" > /dev/null
    docker build -t "$DOCKER_IMAGE:$DOCKER_TAG" .
    popd > /dev/null
}

build_container "fijiOCL" "biodepot/fiji-ocl" \
		"20220713-2010__update20211210__ubuntu_20.04__1fa37497"

