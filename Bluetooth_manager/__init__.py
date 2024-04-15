"""
Bluetooth Manager Package
=========================

Description:
------------
This package provides an interface for managing Bluetooth devices through the `bluetoothctl` command-line tool.
It is engineered to streamline high-level operations such as device discovery, pairing, and connection management,
offering a Pythonic approach to Bluetooth functionality integration. The design abstracts the complexities
associated with direct `bluetoothctl` commands, making it suitable for applications requiring Bluetooth interactions.

Features:
---------
- Device Discovery: Scan for and list available Bluetooth devices in range.
- Device Pairing and Connection Management: Facilitate device pairing and maintain stable connections.
- Concurrent Connection Handling: Manage multiple device connections simultaneously using a thread-safe approach.
- Custom Exception Handling: Specifically designed to capture and report Bluetooth-related errors effectively.

Components:
-----------
- `BluetoothManager`: Core class responsible for initiating scans, connecting, and managing Bluetooth devices.
- `BluetoothManagerError`: Custom exception class tailored for Bluetooth operation errors.

Usage:
------
The package provides a straightforward API to interact with Bluetooth devices. Example usage:

    from bluetooth_manager import BluetoothManager

    # Create an instance with optional channel parameter
    bt_manager = BluetoothManager(channel='1')
    
    # Discover and manage connections
    bt_manager.manage_connections()

Requirements:
-------------
- Python 3.x
- External libraries: subprocess, threading, re, logging, os

Installation:
-------------
Install the package using pip:

    pip install bluetooth-manager

or directly from the source:

    python setup.py install

Version:
--------
0.1.0

Authors:
--------
Ant O,Greene (anthonygreene2007@gmail.com)
"""

__version__ = '0.1.0'
from .manager import BluetoothManager, BluetoothManagerError

__all__ = ['BluetoothManager', 'BluetoothManagerError']