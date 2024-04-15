# Bluetooth Manager Package

![Bluetooth Manager](https://github.com/LoQiseaking69/BT_manager/blob/main/BTmanager.PNG)

## Overview
The `bluetooth_manager` package is designed for programmable Bluetooth device management via `bluetoothctl` on compatible systems. It provides a powerful interface for integrating Bluetooth capabilities into larger applications or for standalone usage, ensuring high-level control and efficient management of Bluetooth devices.

## Features
- **Device Scanning**: Rapid detection of all nearby Bluetooth devices in discoverable mode.
- **Concurrent Connections**: Supports managing multiple connections simultaneously with a configurable cap to balance system load.
- **Error Handling**: Robust custom exceptions and detailed logging facilitate troubleshooting and enhance operational visibility.

## Installation
To install `bluetooth_manager`, execute the provided `Build.sh` shell script, which streamlines the setup process. This script ensures that all prerequisites are met and installs the package within a virtual environment.

1. Ensure the script is executable:
    ```bash
    chmod +x Build.sh
    ```
2. Run the script:
    ```bash
    ./Build.sh
    ```
______________________________________
![screenshot](https://github.com/LoQiseaking69/BT_manager/blob/main/IMG_9452.jpeg)
______________________________________
The script will check for Python 3.6+, install the necessary dependencies, and set up the package. Make sure to have `bluetoothctl` installed on your Linux system for the package to function correctly.

## Dependencies
- Python 3.6 or later.
- Standard Python libraries including `subprocess`, `threading`, `logging`, and `re` for regex processing.
- A system-wide installation of `bluetoothctl`.

## Usage
Incorporate `bluetooth_manager` in your Python scripts as follows:

1. Import `BluetoothManager`:
    ```python
    from bluetooth_manager.manager import BluetoothManager
    ```

2. Create an instance of `BluetoothManager`:
    ```python
    bluetooth_manager = BluetoothManager()
    ```

3. Initiate device connection management:
    ```python
    bluetooth_manager.manage_connections()
    ```

## Example
Here's a straightforward example of initializing the manager and starting the device connection process:

```python
from bluetooth_manager.manager import BluetoothManager

# Initialize the manager with a limit of four concurrent connections
bluetooth_manager = BluetoothManager(max_connections=4)

# Begin the connection management process
bluetooth_manager.manage_connections()
```
