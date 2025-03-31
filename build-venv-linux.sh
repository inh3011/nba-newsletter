#!/bin/bash

if [ -d "venv_linux" ]; then
    echo "venv already exists"
    exit 1
fi

# Create a virtual environment
python3 -m venv venv_linux

# Activate the virtual environment
source venv_linux/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
