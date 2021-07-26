#!/bin/bash

# Get script parent folder path and cd into him
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Activate venv and run application
source venv/bin/activate
python main.py
