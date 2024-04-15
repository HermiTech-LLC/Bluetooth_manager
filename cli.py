import argparse
import sys
from manager import BluetoothManager, BluetoothManagerError, load_config

def main():
    # Define the command-line arguments
    parser = argparse.ArgumentParser(description='CLI tool for managing Bluetooth devices using specified channels.')
    parser.add_argument(
        '--manage', action='store_true',
        help='Activate to start managing Bluetooth devices.'
    )
    parser.add_argument(
        '--channel', type=int, choices=range(1, 4),
        help='Specify the channel for managing Bluetooth devices (1, 2, or 3).'
    )

    args = parser.parse_args()

    # Check if the manage flag is active; then proceed
    if args.manage:
        if args.channel is None:
            print("Error: A channel must be specified to manage devices.", file=sys.stderr)
            sys.exit(1)

        try:
            # Load the base configuration
            config = load_config()
            channel_key = f'channel_{args.channel}'

            # Check if the specified channel configuration exists
            if channel_key not in config:
                print(f"Error: No configuration found for channel {args.channel}.", file=sys.stderr)
                sys.exit(1)

            # Initialize the BluetoothManager with the specific channel configuration
            bluetooth_manager = BluetoothManager(channel=args.channel)
            bluetooth_manager.manage_connections()
            print("Bluetooth device management has started successfully.")
        except BluetoothManagerError as e:
            print(f"Bluetooth Manager Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
