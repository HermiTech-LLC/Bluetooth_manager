# Bluetooth Manager Package

## Overview
The `bluetooth_manager` package offers programmable control over Bluetooth device connections on systems with `bluetoothctl`. This versatile tool can be seamlessly integrated into larger applications or used independently to efficiently manage Bluetooth devices. It is designed to handle multiple connections simultaneously, ensuring robust operations across various environments.

## Features
- **Device Scanning**: Detects all nearby Bluetooth devices that are discoverable.
- **Connection Management**: Enables simultaneous connections to multiple devices, with a configurable limit to ensure system stability and performance.
- **Robust Error Handling**: Utilizes custom exceptions and extensive logging to aid in effective troubleshooting and operational tracking.

## Installation
Install the `bluetooth_manager` by navigating to the package directory and running the following command in your terminal:

```bash
pip install .
```

This installation procedure assumes a Python environment version 3.6 or higher, due to specific language and library requirements.

## Dependencies
- Requires Python 3.6 or higher.
- Utilizes Python's standard libraries: `subprocess`, `threading`, `logging`, and `re` for regular expressions.
- Dependent on `bluetoothctl` being installed on your Linux system, as the package interfaces directly with this tool.

## Usage
To use the `bluetooth_manager` in your Python scripts, follow these steps:

1. **Import the BluetoothManager**:
    ```python
    from bluetooth_manager.manager import BluetoothManager
    ```

2. **Create an instance of BluetoothManager**:
    ```python
    bluetooth_manager = BluetoothManager()
    ```

3. **Manage Bluetooth Connections**:
    ```python
    bluetooth_manager.manage_connections()
    ```

This process initiates scanning for devices and manages connections based on the predetermined limits set during the initialization of `BluetoothManager`.

## Example
Here is a simple example demonstrating how to set up the manager and initiate connections:

```python
from bluetooth_manager.manager import BluetoothManager

# Set up the manager with a maximum of 4 concurrent connections
bluetooth_manager = BluetoothManager(max_connections=4)

# Start managing connections
bluetooth_manager.manage_connections()
```

## Contributing
We welcome contributions to the `bluetooth_manager` package. We ask that contributors adhere to best coding practices, provide clear annotations where necessary, and maintain the integrity and structure of the existing codebase.

## Contact
For any inquiries, please contact:
- **Name**: Ant
- **Email**: anthonygreene2007@gmail.com