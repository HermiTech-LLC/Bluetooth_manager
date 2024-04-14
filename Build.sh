#!/bin/bash

# This script deploys the bluetooth_manager package on a Raspberry Pi 4B.
# It checks for the required version of Python, installs bluetoothctl if missing,
# and sets up the package for managing Bluetooth devices.

# Exit immediately if a command exits with a non-zero status.
set -e

# Echoes and executes a command, displaying it for debugging
exec_cmd() {
    echo "+ $@"
    "$@"
}

# Check and install Python 3.6 or higher
echo "Checking for Python 3.6+ installation..."
if ! command -v python3 &>/dev/null || [ $(python3 -c 'import sys; print(sys.version_info[:2] >= (3, 6))') != "True" ]; then
    echo "Python 3.6+ is not installed. Installing Python..."
    exec_cmd sudo apt-get update
    exec_cmd sudo apt-get install -y python3 python3-pip
else
    echo "Python 3.6+ is already installed."
fi

# Ensure bluetoothctl is installed
echo "Checking for bluetoothctl..."
if ! command -v bluetoothctl &>/dev/null; then
    echo "bluetoothctl not found. Installing bluetooth packages..."
    exec_cmd sudo apt-get install -y bluez
else
    echo "bluetoothctl is already installed."
fi

# Navigate to the directory containing the package
echo "Navigating to the package directory..."
exec_cmd cd "$(dirname "$0")"

# Install the bluetooth_manager package
echo "Installing the bluetooth_manager package..."
exec_cmd pip3 install .

# Optionally, run a script to test the installation
echo "Running a test to ensure everything is set up correctly..."
exec_cmd python3 -c "from bluetooth_manager.manager import BluetoothManager; manager = BluetoothManager(); print('Setup successful if no errors appear!')"

echo "Deployment complete. The bluetooth_manager is ready to use."