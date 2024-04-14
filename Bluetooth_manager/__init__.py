"""
Bluetooth Manager Package.

This package provides classes and utilities to manage Bluetooth devices using
the bluetoothctl tool from the command line.
"""

__version__ = '0.1.0'
from .manager import BluetoothManager, BluetoothManagerError

__all__ = ['BluetoothManager', 'BluetoothManagerError']