#!/bin/bash

# Update system and install required packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip unzip python3-venv libpq-dev

# Create a system user for the application
sudo groupadd legacy
sudo useradd -r -g legacy -s /usr/sbin/nologin legacy -d /home/legacy

# Create the user's home directory
sudo mkdir -p /home/legacy/
sudo chown legacy:legacy /home/legacy/

# Copy MentalHealthCounsellor.zip to the appropriate location
sudo cp /tmp/MentalHealthCounsellor.zip /home/legacy/MentalHealthCounsellor.zip

# Navigate to the user directory
cd /home/legacy/

# Unzip the MentalHealthCounsellor.zip file
sudo unzip MentalHealthCounsellor.zip -d /home/legacy/MentalHealthCounsellor

# Change ownership of the MentalHealthCounsellor directory to the correct user
sudo chown -R legacy:legacy /home/legacy/MentalHealthCounsellor/

# Remove any existing virtual environment
sudo -u legacy bash -c 'rm -rf /home/legacy/MentalHealthCounsellor/venv'

# Create a new virtual environment
sudo -u legacy bash -c 'python3 -m venv /home/legacy/MentalHealthCounsellor/venv'

# Activate the virtual environment and install requirements
sudo -u legacy bash -c 'source /home/legacy/MentalHealthCounsellor/venv/bin/activate && pip install --upgrade pip && pip install -r /home/legacy/MentalHealthCounsellor/requirements.txt'

# Creating a .env file in the application directory
sudo -u legacy bash -c 'cd /home/legacy/MentalHealthCounsellor/app touch .env'

# Copy the systemd service file for the web application
sudo cp /home/legacy/MentalHealthCounsellor/sys-service/MentalHealthCounsellor.service /etc/systemd/system/MentalHealthCounsellor.service

# Reload systemd to register the new service
sudo systemctl daemon-reload

# Enable the MentalHealthCounsellor service to start at boot
sudo systemctl enable MentalHealthCounsellor.service

# Start the MentalHealthCounsellor service
sudo systemctl start MentalHealthCounsellor.service

# Change ownership of all files in /home/legacy to ensure correct user permissions
sudo chown -R legacy:legacy /home/legacy/

# Check the status of the MentalHealthCounsellor service
sudo systemctl status MentalHealthCounsellor.service