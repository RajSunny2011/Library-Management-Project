#!/bin/bash
# Bash script to set up a Python virtual environment and install required packages

# Set the virtual environment name
VENV_NAME="venv"

# Check if the virtual environment folder exists
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_NAME
fi

# Activate the virtual environment
source "$VENV_NAME/bin/activate"

# Install required packages from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping installation."
fi

echo "Setup complete."
echo "The virtual environment is now active. You can deactivate it by typing 'deactivate'."
echo

# Wait for user input before closing terminal
read -p "Press any key to continue..." -n1 -s
echo
