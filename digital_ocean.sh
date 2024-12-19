#!/bin/bash

# Update and upgrade system
sudo apt update && sudo apt upgrade -y
 
# Install requirements
sudo apt install -y python3 python3-pip unzip postgresql python3-venv libpq-dev
 
# Unzip webapp #replace with downloaded directory name
unzip MentalHealthCounsellor-main.zip

# Change into the webapp directory
cd MentalHealthCounsellor-main

# Remove existing venv if it exists
rm -rf venv 

# Setup virtual environment
python3 -m venv venv
. venv/bin/activate
 
# Upgrade pip
pip install --upgrade pip
 
# Install Python dependencies
pip install -r requirements.txt

cd app

# create .env file
touch .env

# Add the following to the .env file
echo "GROQ_API_KEY=" > .env
 
cd ..

# Start Django server
streamlit run app/main.py