#!/bin/bash
# This script assembles the application for uploading to the file repository
# and for then deploying to devices.

# Get the name and version of this application in config.txt
applicationName=`grep applicationName config.txt | grep -v "#" | head -1 | cut -d'=' -f 2`
applicationVersion=`grep applicationVersion config.txt | grep -v "#" | head -1 | cut -d'=' -f 2`
echo "Starting build for Application ${applicationName}, Version: ${applicationVersion}"
cd `dirname $0`

# When tarring, exclude any existing tar.gz files of artifacts
tar --gzip --exclude="${applicationName}_*tar.gz" -cf "./${applicationName}_${applicationVersion}.tar.gz" .

# Finished
echo "Finished installation procedure for Application ${applicationName}, Version: ${applicationVersion}"
echo "Please upload the artifact (${applicationName}_${applicationVersion}.tar.gz) to the file repository for deploying to devices."

