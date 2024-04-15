#!/bin/bash

# Enhanced deployment script for bluetooth_manager on a Raspberry Pi

set -eo pipefail
log_file="deploy_bluetooth_manager.log"
echo "Deployment started at $(date)" > $log_file

exec_cmd() {
    echo "+ $@" | tee -a $log_file
    eval "$@" 2>&1 | tee -a $log_file
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Preparing to deploy the bluetooth_manager package..." | tee -a $log_file

# Ensure necessary tools and libraries are installed
echo "Checking for required system tools..." | tee -a $log_file

if ! command_exists python3 || ! command_exists pip3; then
    echo "Python or pip is not installed, installing them..." | tee -a $log_file
    exec_cmd "sudo apt-get update"
    exec_cmd "sudo apt-get install -y python3 python3-pip"
else
    echo "Python and pip are already installed." | tee -a $log_file
fi

# Ensure wheel is installed for building packages
if ! pip3 list | grep -q wheel; then
    echo "Installing wheel..." | tee -a $log_file
    exec_cmd "pip3 install wheel"
else
    echo "Wheel is already installed." | tee -a $log_file
fi

# Ensure bluetoothctl is available
if ! command_exists bluetoothctl; then
    echo "bluetoothctl not available, installing bluez..." | tee -a $log_file
    exec_cmd "sudo apt-get install -y bluez"
else
    echo "bluetoothctl is available." | tee -a $log_file
fi

# Setup and activate the virtual environment
echo "Setting up the virtual environment..." | tee -a $log_file
exec_cmd "python3 -m venv venv"
source venv/bin/activate

# Install the package
echo "Installing the bluetooth_manager package..." | tee -a $log_file
exec_cmd "pip3 install ."

# Verify the installation by attempting to import the package
echo "Verifying the installation..." | tee -a $log_file
if python3 -c "from Bluetooth_manager.manager import BluetoothManager; print('Import successful')" > /dev/null 2>&1; then
    echo "Installation verified successfully." | tee -a $log_file
else
    echo "Failed to verify the installation. Check logs for details." | tee -a $log_file
    exit 1
fi

echo "Deployment completed successfully." | tee -a $log_file