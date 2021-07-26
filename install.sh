#!/bin/bash

# Get project folder path and cd into it 
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Create a venv
python3 -m venv venv
# Activate it
source venv/bin/activate
# Install modules
pip install -r requirements.txt

# Make run.sh executable
chmod +x run.sh

# Create an alias to run the application from terminal from everywhere
echo "alias oplinux='$parent_path/run.sh'" >> file_to_append_to
