import yaml
import subprocess
import time
import threading
import logging
import re
from queue import Queue, Empty

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = load_config()['bluetooth_manager']

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
        self.bluetoothctl_path = config['bluetoothctl_path']
        self.max_connections = config['max_connections']
        self.connection_semaphore = threading.Semaphore(self.max_connections)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=config['logging']['file'],
            level=getattr(logging, config['logging']['level']),
            format=config['logging']['format']
        )

    def run_bluetoothctl_command(self, command, wait_time=None):
        """Execute a command in the bluetoothctl environment and handle its output."""
        wait_time = wait_time or config['scan']['timeout_seconds']
        process = subprocess.Popen(
            [self.bluetoothctl_path],
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        try:
            process.stdin.write(f"{command}\n")
            process.stdin.flush()
            time.sleep(wait_time)
            process.stdin.write("exit\n")
            process.stdin.flush()
            output, errors = process.communicate()
            if errors:
                raise BluetoothManagerError("Error executing command.", command, errors)
            return output
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            raise BluetoothManagerError("Command timeout. Bluetooth operation did not respond in time.", command)
        finally:
            process.terminate()

    def discover_devices(self):
        """Scan for available Bluetooth devices and return a list of device MAC addresses."""
        logging.info("Scanning for available Bluetooth devices...")
        output = self.run_bluetoothctl_command("scan on")
        devices = re.findall(config['scan']['device_regex'], output)
        logging.info(f"Devices found: {devices}")
        return devices

    def connect_device(self, device_mac):
        """Connect to a specific Bluetooth device using a semaphore to limit concurrent connections."""
        with self.connection_semaphore:
            logging.info(f"Attempting to connect to {device_mac}...")
            output = self.run_bluetoothctl_command(
                f"connect {device_mac}", 
                wait_time=config['connection']['response_timeout']
            )
            if config['connection']['expected_response'] in output:
                logging.info(f"Successfully connected to {device_mac}.")
            else:
                logging.error(f"Failed to connect to {device_mac}.")

    def manage_connections(self):
        """Manage connections to discovered devices."""
        devices = self.discover_devices()
        threads = []
        for device_mac in devices[:self.max_connections]:  # Limit the number of devices to manage based on the semaphore
            thread = threading.Thread(target=self.connect_device, args=(device_mac,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        logging.info("All device connection attempts are complete.")

# Instantiate and use BluetoothManager
bluetooth_manager = BluetoothManager()
bluetooth_manager.manage_connections()