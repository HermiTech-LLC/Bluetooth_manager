"""
Bluetooth Manager Package
=========================

This package provides classes and utilities to manage Bluetooth devices using
Windows PowerShell commands. It is designed to facilitate high-level
management and automation of Bluetooth operations such as device discovery,
pairing, and connection management in a Pythonic way.

The package abstracts the complexity of direct interactions with the Windows
Bluetooth API and provides an easy-to-use interface that can be integrated into
larger applications that require Bluetooth capability.

Main Components:
- `BluetoothManager`: A class to handle scanning, connecting, and managing Bluetooth devices using PowerShell.
- `BluetoothManagerError`: Custom exception class for handling Bluetooth-related errors.
"""

__version__ = '0.1.0'
from .manager import BluetoothManager, BluetoothManagerError

__all__ = ['BluetoothManager', 'BluetoothManagerError']
