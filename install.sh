#!/bin/bash
# This script installs the application as a systemd service so it continuously runs
# It assumes there is an app.service file in the current directory and
# the name of the service is in the config.txt file in this directory
#

cd `dirname $0`
installationDir=`pwd`

# Get the name for this application in config.txt
applicationName=`grep applicationName ./config.txt | grep -v "#" | head -1 | cut -d'=' -f 2`

echo "Starting installation for Application ${applicationName}"

# Install any python libraries which may be listed in the requirements.txt file
# Optional: if pip not already available: sudo apt-get install python-pip
pip install -r ./requirements.txt

# Replace the service name in the .service file
sed -i "s|\[\[applicationName\]\]|${applicationName}|g" ./app.service
sed -i "s|\[\[installationDir\]\]|${installationDir}|g" ./app.service
# Install this application as a systemd service
echo "Installing as a systemd service"
sudo cp "./app.service" "/lib/systemd/system/${applicationName}.service"
sudo chmod 644  /lib/systemd/system/${applicationName}.service
sudo systemctl daemon-reload
sudo systemctl enable "${applicationName}.service"
sudo systemctl start "${applicationName}.service"
sudo systemctl restart "${applicationName}.service"

# Finished
echo "Finished installation procedure for Application ${applicationName}"

