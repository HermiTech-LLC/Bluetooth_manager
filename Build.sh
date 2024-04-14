#!/bin/bash

# This script deploys the bluetooth_manager package on a Raspberry Pi 4B.
# It verifies and installs the necessary Python and bluetoothctl if missing,
# then installs and tests the package for managing Bluetooth devices within a virtual environment.

# Exit if any command fails and enable verbose output for debugging
set -eo pipefail

# Function to echo and execute commands
exec_cmd() {
    echo "+ $@"
    eval "$@"
}

# Helper function to check command existence
command_exists() {
    command -v "$1" &>/dev/null
}

echo "Starting deployment of bluetooth_manager package..."

# Check and install Python 3.6 or higher
echo "Checking for Python 3.6+ installation..."
if ! command_exists python3 || [[ $(python3 -c 'import sys; print(sys.version_info >= (3, 6))') != "True" ]]; then
    echo "Python 3.6+ is not installed. Installing Python..."
    exec_cmd "sudo apt-get update"
    exec_cmd "sudo apt-get install -y python3 python3-pip"
else
    echo "Python 3.6+ is already installed."
fi

# Ensure bluetoothctl is installed
echo "Checking for bluetoothctl..."
if ! command_exists bluetoothctl; then
    echo "bluetoothctl not found. Installing bluetooth packages..."
    exec_cmd "sudo apt-get install -y bluez"
else
    echo "bluetoothctl is already installed."
fi

# Ensure virtual environment is present and activated
echo "Setting up virtual environment for package installation..."
if [ ! -d "venv" ]; then
    exec_cmd "python3 -m venv venv"
else
    echo "Virtual environment already exists."
fi
source venv/bin/activate

# Navigate to the directory containing the package
echo "Navigating to the package directory..."
cd "$(dirname "$0")"

# Install the bluetooth_manager package
echo "Installing the bluetooth_manager package..."
exec_cmd "pip3 install ."

# Optionally, run a script to test the installation
echo "Running a test to ensure everything is set up correctly..."
exec_cmd "python3 -c 'from bluetooth_manager.manager import BluetoothManager; manager = BluetoothManager(); print(\"Setup successful if no errors appear!\")'"

echo "Deployment complete. The bluetooth_manager is ready to use."