# Bluetooth Manager Package

## Overview
The `bluetooth_manager` package allows you to manage Bluetooth device connections programmatically on systems with `bluetoothctl` installed. This package is designed to handle multiple Bluetooth connections simultaneously and can be integrated into larger applications or used standalone for managing Bluetooth devices.

## Features
- **Device Scanning**: Scan for all available Bluetooth devices nearby.
- **Connection Management**: Connect to multiple devices concurrently, with a configurable limit on the number of simultaneous connections.
- **Robust Error Handling**: Custom exceptions and detailed logging for tracking and debugging.

## Installation
To install the `bluetooth_manager`, navigate to the package directory and run the following command:

```bash
pip install .
```

This will install the package into your Python environment. Ensure that your Python version is 3.6 or higher due to syntax and library requirements.

## Dependencies
- Python 3.6 or higher
- `subprocess`, `threading`, `logging`, `re` (regular expressions) â All from the Python standard library.
- Ensure `bluetoothctl` is installed on your Linux system as this package interfaces directly with it.

## Usage
To use the `bluetooth_manager` in your Python scripts, follow these steps:

1. **Import the BluetoothManager**:
    ```python
    from bluetooth_manager.manager import BluetoothManager
    ```

2. **Create an Instance**:
    ```python
    bluetooth_manager = BluetoothManager()
    ```

3. **Manage Connections**:
    ```python
    bluetooth_manager.manage_connections()
    ```

This will start scanning for devices and attempt to connect to them based on the available slots for connections defined during the initialization of `BluetoothManager`.

## Example
Here's a simple example demonstrating how to start the manager and initiate connections:

```python
from bluetooth_manager.manager import BluetoothManager

# Initialize the manager with a maximum of 4 concurrent connections
bluetooth_manager = BluetoothManager(max_connections=4)

# Start managing connections
bluetooth_manager.manage_connections()
```

## Contributing
Contributions to the `bluetooth_manager` package are welcome! Please ensure to follow standard coding practices, add comments where necessary, and maintain the structure and quality of the code.


## Contact
For direct inquiries, contact:
- **Name**: Ant
- **Email**: anthonygreene2007@gmail.com
