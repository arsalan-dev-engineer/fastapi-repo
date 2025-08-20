
#!/bin/bash
# This script sets up a Python virtual environment and installs required packages.
echo "Setting up the Python virtual environment..."
# Create a virtual environment named 'venv' 
python3 -m venv venv
echo "Activating the virtual environment..."
# Activate the virtual environment
source venv/bin/activate
echo "Installing required packages..."
# Install the required packages from requirements.txt
pip install -r requirements.txt
echo "Setup complete. The virtual environment is ready to use."
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To deactivate the virtual environment, run: deactivate"

