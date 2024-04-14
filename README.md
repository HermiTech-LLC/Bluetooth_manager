# Bluetooth Manager Package

## Overview
The `bluetooth_manager` package enables programmatic management of Bluetooth device connections on systems equipped with `bluetoothctl`. Designed for versatility, it can be integrated into broader applications or utilized standalone to oversee Bluetooth devices efficiently. It handles multiple connections concurrently, ensuring smooth operations across various devices.

## Features
- **Device Scanning**: Scans for all detectable Bluetooth devices within range.
- **Connection Management**: Facilitates connections to multiple devices simultaneously, featuring a configurable limit on the number of concurrent connections to ensure system stability.
- **Robust Error Handling**: Implements custom exceptions and provides comprehensive logging to facilitate effective tracking and troubleshooting.

## Installation
To install the `bluetooth_manager`, navigate to the package directory and execute the following command in your terminal:

```bash
pip install .
```

This command installs the package into your Python environment. Compatibility requires Python version 3.6 or higher due to specific syntax and library dependencies.

## Dependencies
- Python 3.6 or higher
- Standard Python libraries: `subprocess`, `threading`, `logging`, `re` (regular expressions)
- `bluetoothctl` must be installed on your Linux system as this package directly interfaces with it.

## Usage
Incorporate the `bluetooth_manager` into your Python scripts with these steps:

1. **Import BluetoothManager**:
    ```python
    from bluetooth_manager.manager import BluetoothManager
    ```

2. **Instantiate the Manager**:
    ```python
    bluetooth_manager = BluetoothManager()
    ```

3. **Execute Connection Management**:
    ```python
    bluetooth_manager.manage_connections()
    ```

This initiates a device scanning process and manages connections based on the configured concurrent connection slots during the `BluetoothManager` initialization.

## Example
Below is a straightforward example to demonstrate how to initialize the manager and manage connections:

```python
from bluetooth_manager.manager import BluetoothManager

# Initialize the manager allowing up to 4 concurrent connections
bluetooth_manager = BluetoothManager(max_connections=4)

# Begin connection management
bluetooth_manager.manage_connections()
```

## Contributing
Contributions are encouraged and appreciated. Please adhere to standard coding practices, annotate code clearly where needed, and uphold the existing codebase structure and quality.

## Contact
For direct inquiries, please contact:
- **Name**: Ant
- **Email**: anthonygreene2007@gmail.com