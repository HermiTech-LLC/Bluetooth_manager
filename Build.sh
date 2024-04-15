#!/bin/bash

# Enhanced script for deploying the bluetooth_manager package on a Raspberry Pi 4B.
# It verifies and installs the necessary dependencies, manages virtual environments,
# and provides detailed feedback and options to the user.

# Exit if any command fails and enable verbose output for debugging
set -eo pipefail

# Initialize log file
log_file="deploy_bluetooth_manager.log"
echo "Deployment log - $(date)" > $log_file

# Function to echo, execute commands, and log output
exec_cmd() {
    echo "+ $@" | tee -a $log_file
    eval "$@" 2>&1 | tee -a $log_file
}

# Helper function to check command existence
command_exists() {
    command -v "$1" &>/dev/null
}

# Start deployment
echo "Starting deployment of the bluetooth_manager package..." | tee -a $log_file

# Option parsing for skipping certain steps
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-python) skip_python="yes"; shift ;;
        --skip-bluetoothctl) skip_bluetoothctl="yes"; shift ;;
        --venv-path) venv_path="$2"; shift; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
done

# Check and install Python 3.6 or higher
if [ "$skip_python" != "yes" ]; then
    echo "Checking for Python 3.6+ installation..." | tee -a $log_file
    if ! command_exists python3 || [[ $(python3 -c 'import sys; print(sys.version_info >= (3, 6))') != "True" ]]; then
        echo "Python 3.6+ is not installed. Installing Python..." | tee -a $log_file
        exec_cmd "sudo apt-get update"
        exec_cmd "sudo apt-get install -y python3 python3-pip"
    else
        echo "Python 3.6+ is already installed." | tee -a $log_file
    fi
fi

# Ensure bluetoothctl is installed
if [ "$skip_bluetoothctl" != "yes" ]; then
    echo "Checking for bluetoothctl..." | tee -a $log_file
    if ! command_exists bluetoothctl; then
        echo "bluetoothctl not found. Installing bluetooth packages..." | tee -a $log_file
        exec_cmd "sudo apt-get install -y bluez"
    else
        echo "bluetoothctl is already installed." | tee -a $log_file
    fi
fi

# Ensure virtual environment is present and activated
venv_path="${venv_path:-venv}"
echo "Setting up virtual environment at $venv_path for package installation..." | tee -a $log_file
if [ ! -d "$venv_path" ]; then
    exec_cmd "python3 -m venv $venv_path"
else
    echo "Virtual environment already exists at $venv_path." | tee -a $log_file
fi
source $venv_path/bin/activate

# Navigate to the directory containing the package
echo "Navigating to the package directory..." | tee -a $log_file
cd "$(dirname "$0")"

# Install the bluetooth_manager package
echo "Installing the bluetooth_manager package..." | tee -a $log_file
exec_cmd "pip3 install ."

# Optionally, run a script to test the installation
echo "Running a test to ensure everything is set up correctly..." | tee -a $log_file
exec_cmd "python3 -c 'from bluetooth_manager.manager import BluetoothManager; manager = BluetoothManager(); print(\"Setup successful if no errors appear!\")'"

echo "Deployment complete. The bluetooth_manager is ready to use." | tee -a $log_file