import yaml
import subprocess
import time
import threading
import logging
import re  # Import re module to use regular expressions for device parsing
from queue import Queue, Empty

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BluetoothManagerError(Exception):
    """Custom exception for BluetoothManager errors."""

    def __init__(self, message, command=None, errors=None):
        super().__init__(message)
        self.message = message
        self.command = command
        self.errors = errors

    def __str__(self):
        error_message = f"{self.message}\nCommand: {self.command}\nErrors: {self.errors}"
        return error_message

class BluetoothManager:
    """Manage Bluetooth operations with dynamic device handling and concurrent connection limits."""
    
    def __init__(self, max_connections=4):
        self.bluetoothctl_path = 'bluetoothctl'
        self.max_connections = max_connections if max_connections else config.get('max_connections', 4)
        self.connection_semaphore = threading.Semaphore(self.max_connections)  # Limits the number of concurrent connections

    def run_bluetoothctl_command(self, command, wait_time=1, expect_response=None):
        """Execute a command in the bluetoothctl environment and handle its output."""
        process = subprocess.Popen([self.bluetoothctl_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            process.stdin.write(f"{command}\n")
            process.stdin.flush()
            if wait_time:
                time.sleep(wait_time)
            process.stdin.write("exit\n")
            process.stdin.flush()
            output, errors = process.communicate(timeout=10)
            if errors:
                logging.error(f"Error: {errors}")
                raise BluetoothManagerError("Error executing command.", command, errors)
            if expect_response and expect_response not in output:
                logging.warning(f"Expected '{expect_response}' not found in the output.")
            return output or ""
        except subprocess.TimeoutExpired:
            logging.error("Command timeout. Bluetooth operation did not respond in time.")
            process.kill()
            output, _ = process.communicate()
            return output or ""
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise BluetoothManagerError("An exception occurred while running the command.", command, str(e))
        finally:
            process.terminate()

    def discover_devices(self):
        """Scan for available Bluetooth devices and return a list of device MAC addresses."""
        logging.info("Scanning for available Bluetooth devices...")
        output = self.run_bluetoothctl_command("scan on", wait_time=10)
        devices = re.findall(r'Device (\S+) ', output)
        logging.info(f"Devices found: {devices}")
        return devices

    def connect_device(self, device_mac):
        """Connect to a specific Bluetooth device using a semaphore to limit concurrent connections."""
        with self.connection_semaphore:
            logging.info(f"Attempting to connect to {device_mac}...")
            response = self.run_bluetoothctl_command(f"connect {device_mac}", wait_time=5, expect_response="Connection successful")
            if "Connection successful" in response:
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