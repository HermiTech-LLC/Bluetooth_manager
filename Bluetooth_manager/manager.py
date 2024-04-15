import yaml
import subprocess
import time
import threading
import logging
import re
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def load_config(channel='default'):
    config_path = os.getenv('BLUETOOTH_MANAGER_CONFIG', 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)['bluetooth_manager']
        channel_config = config.get(f'channel_{channel}', {})
        return {**config['default'], **channel_config}
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing the configuration file: {e}")
        raise

class BluetoothManagerError(Exception):
    def __init__(self, message, command=None, errors=None):
        super().__init__(message)
        self.command = command
        self.errors = errors

    def __str__(self):
        error_details = f"Command: {self.command}, Errors: {self.errors}" if self.errors else "No additional error details."
        return f"{self.message}\n{error_details}"

class BluetoothManager:
    def __init__(self, channel='default'):
        self.config = load_config(channel)
        self.bluetoothctl_path = self.config['bluetoothctl_path']
        self.max_connections = self.config['max_connections']
        self.executor = ThreadPoolExecutor(max_workers=self.max_connections)
        self.setup_logging()

    def setup_logging(self):
        log_path = Path(self.config['logging']['file'])
        os.makedirs(log_path.parent, exist_ok=True)
        logging.basicConfig(filename=str(log_path), level=logging.INFO, format=self.config['logging']['format'])

    def run_bluetoothctl_command(self, command, wait_time=None):
        wait_time = wait_time or self.config['scan']['timeout_seconds']
        env = os.environ.copy()
        with subprocess.Popen([self.bluetoothctl_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env) as process:
            try:
                process.stdin.write(f"{command}\nexit\n")
                process.stdin.flush()
                stdout, stderr = process.communicate(timeout=wait_time)
                if stderr:
                    raise BluetoothManagerError("Error executing command", command, stderr)
                return stdout
            except subprocess.TimeoutExpired:
                process.kill()
                raise BluetoothManagerError("Command timeout", command)

    def discover_devices(self):
        output = self.run_bluetoothctl_command("scan on")
        devices = re.findall(self.config['scan']['device_regex'], output)
        return devices

    def connect_device(self, device_mac):
        try:
            output = self.run_bluetoothctl_command(f"connect {device_mac}", self.config['connection']['response_timeout'])
            if self.config['connection']['expected_response'] in output:
                logging.info(f"Successfully connected to {device_mac}.")
            else:
                logging.error(f"Failed to connect to {device_mac}.")
        except BluetoothManagerError as e:
            logging.error(str(e))

    def manage_connections(self):
        devices = self.discover_devices()
        futures = [self.executor.submit(self.connect_device, mac) for mac in devices[:self.max_connections]]
        for future in futures:
            future.result()  # This ensures we wait for all tasks to complete
        logging.info("All device connection attempts are complete.")

# Example usage:
bluetooth_manager = BluetoothManager(channel='1')
bluetooth_manager.manage_connections()