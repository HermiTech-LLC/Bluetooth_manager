#!/bin/bash

# This script deploys the bluetooth_manager package on a Raspberry Pi 4B.
# It verifies and installs the necessary Python and bluetoothctl if missing,
# then installs and tests the package for managing Bluetooth devices.

# Exit if any command fails and enable verbose output for debugging
set -eo pipefail

# Function to echo and execute commands
exec_cmd() {
    echo "+ $@"
    eval "$@"
}

# Check and install Python 3.6 or higher
echo "Checking for Python 3.6+ installation..."
if ! python3 --version &>/dev/null || [[ $(python3 -c 'import sys; print(sys.version_info >= (3, 6))') != "True" ]]; then
    echo "Python 3.6+ is not installed. Installing Python..."
    exec_cmd "sudo apt-get update"
    exec_cmd "sudo apt-get install -y python3 python3-pip"
else
    echo "Python 3.6+ is already installed."
fi

# Ensure bluetoothctl is installed
echo "Checking for bluetoothctl..."
if ! command -v bluetoothctl &>/dev/null; then
    echo "bluetoothctl not found. Installing bluetooth packages..."
    exec_cmd "sudo apt-get install -y bluez"
else
    echo "bluetoothctl is already installed."
fi

# Navigate to the directory containing the package
echo "Navigating to the package directory..."
exec_cmd "cd $(dirname "$0")"

# Install the bluetooth_manager package
echo "Installing the bluetooth_manager package..."
exec_cmd "pip3 install ."

# Optionally, run a script to test the installation
echo "Running a test to ensure everything is set up correctly..."
exec_cmd "python3 -c 'from bluetooth_manager.manager import BluetoothManager; manager = BluetoothManager(); print(\"Setup successful if no errors appear!\")'"

echo "Deployment complete. The bluetooth_manager is ready to use."