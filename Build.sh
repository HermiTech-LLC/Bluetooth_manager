#!/bin/bash

# Set strict error handling
set -euo pipefail

# Setup logging
log_file="deploy_bluetooth_manager.log"
exec 3>&1 1>>"${log_file}" 2>&1
echo "Deployment started at $(date)"

exec_cmd() {
    echo "+ $@" >&3
    eval "$@"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Preparing to deploy the bluetooth_manager package..." >&3

# Ensure necessary tools and libraries are installed
echo "Checking for required system tools..." >&3

if ! command_exists python3; then
    echo "Python is not installed, installing it..." >&3
    sudo apt-get update
    sudo apt-get install -y python3
fi

if ! command_exists pip3; then
    echo "pip is not installed, installing it..." >&3
    sudo apt-get install -y python3-pip
fi

# Ensure wheel is installed for building packages
if ! pip3 list | grep -q wheel; then
    echo "Installing wheel..." >&3
    pip3 install wheel
else
    echo "Wheel is already installed." >&3
fi

# Ensure bluetoothctl is available
if ! command_exists bluetoothctl; then
    echo "bluetoothctl not available, installing bluez..." >&3
    sudo apt-get install -y bluez
else
    echo "bluetoothctl is available." >&3
fi

# Setup and activate the virtual environment
echo "Setting up the virtual environment..." >&3
python3 -m venv venv
source venv/bin/activate

# Install the package
echo "Installing the bluetooth_manager package..." >&3
pip3 install .

# Verify the installation by attempting to import the package
echo "Verifying the installation..." >&3
if python3 -c "from Bluetooth_manager.manager import BluetoothManager; print('Import successful')" >&3; then
    echo "Installation verified successfully." >&3
else
    echo "Failed to verify the installation. Check logs for details." >&3
    exit 1
fi

echo "Deployment completed successfully." >&3