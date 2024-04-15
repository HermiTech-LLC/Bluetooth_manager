import yaml
import subprocess
import time
import threading
import logging
import re
import os
from pathlib import Path

def load_config():
    try:
        config_path = os.getenv('BLUETOOTH_MANAGER_CONFIG', 'config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)['bluetooth_manager']
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file not found at {}".format(config_path))
    except yaml.YAMLError as e:
        raise RuntimeError("Error parsing the configuration file: " + str(e))

config = load_config()

class BluetoothManagerError(Exception):
    """Custom exception for BluetoothManager errors."""
    def __init__(self, message, command=None, errors=None):
        super().__init__(message)
        self.message = message
        self.command = command
        self.errors = errors

    def __str__(self):
        return f"{self.message}\nCommand: {self.command}\nErrors: {self.errors}"

class BluetoothManager:
    """Manage Bluetooth operations with dynamic device handling and concurrent connection limits."""
    
    def __init__(self):
        self.max_connections = config['max_connections']
        self.connection_semaphore = threading.Semaphore(self.max_connections)
        self.setup_logging()

    def setup_logging(self):
        log_path = Path(config['logging']['file'])
        os.makedirs(log_path.parent, exist_ok=True)
        logging.basicConfig(
            filename=str(log_path),
            level=getattr(logging, config['logging']['level']),
            format=config['logging']['format']
        )

    def run_powershell_command(self, ps_command, wait_time=None):
        """Execute a PowerShell command to manage Bluetooth on Windows."""
        wait_time = wait_time or config['scan']['timeout_seconds']
        command = ['powershell', '-Command', ps_command]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, errors = process.communicate(timeout=wait_time)
            if process.returncode != 0:
                raise BluetoothManagerError("Command failed.", ps_command, errors)
            return output
        except subprocess.TimeoutExpired:
            process.kill()
            _, errors = process.communicate()
            raise BluetoothManagerError("Command timeout. Bluetooth operation did not respond in time.", ps_command, errors)
        finally:
            process.terminate()

    def discover_devices(self):
        """Use PowerShell to scan for available Bluetooth devices."""
        logging.info("Scanning for available Bluetooth devices...")
        ps_command = "Get-PnpDevice -Class Bluetooth | Where-Object {$_.Status -eq 'OK'} | Select-Object -ExpandProperty FriendlyName"
        output = self.run_powershell_command(ps_command)
        devices = re.findall(config['scan']['device_regex'], output)
        logging.info(f"Devices found: {devices}")
        return devices

    def connect_device(self, device_mac):
        """Connect to a specific Bluetooth device using PowerShell."""
        with self.connection_semaphore:
            logging.info(f"Attempting to connect to {device_mac}...")
            ps_command = f"Add-BluetoothDevice -DeviceID '{device_mac}'"
            output = self.run_powershell_command(ps_command, wait_time=config['connection']['response_timeout'])
            if 'connected' in output.lower():
                logging.info(f"Successfully connected to {device_mac}.")
            else:
                logging.error(f"Failed to connect to {device_mac}.")

    def manage_connections(self):
        """Manage connections to discovered devices."""
        devices = self.discover_devices()
        threads = []
        for device_mac in devices[:self.max_connections]:
            thread = threading.Thread(target=self.connect_device, args=(device_mac,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        logging.info("All device connection attempts are complete.")

# Instantiate and use BluetoothManager
bluetooth_manager = BluetoothManager()
bluetooth_manager.manage_connections()
