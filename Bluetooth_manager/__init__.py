# Import key classes and functions from your modules
from .bluetooth_manager import BluetoothManager
from .device_discovery import discover_devices, connect_device
from .config_loader import load_config

# If you have constants or utilities that should be accessible
# from the package, you can also import them here:
from .constants import DEFAULT_TIMEOUT, SUPPORTED_DEVICES

# Optionally, you can define an __all__ list which specifies what
# symbols will be exported when 'from package import *' is used.
__all__ = [
    'BluetoothManager',
    'discover_devices',
    'connect_device',
    'load_config',
    'DEFAULT_TIMEOUT',
    'SUPPORTED_DEVICES'
]