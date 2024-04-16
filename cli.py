import argparse
import sys
from Bluetooth_manager.manager import BluetoothManager, BluetoothManagerError

def main():
    parser = argparse.ArgumentParser(
        description='CLI tool for managing Bluetooth devices using specified channels.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--manage', action='store_true',
        help='Manage connections automatically. Requires --channel.'
    )
    parser.add_argument(
        '--scan', action='store_true',
        help='Scan for available Bluetooth devices. Can be used with --channel.'
    )
    parser.add_argument(
        '--connect', metavar='MAC', type=str,
        help='Connect to a specific Bluetooth device by MAC address. Requires --channel.'
    )
    parser.add_argument(
        '--disconnect', action='store_true',
        help='Disconnect all devices. Requires --channel.'
    )
    parser.add_argument(
        '--list', action='store_true',
        help='List all connected devices. Requires --channel.'
    )
    parser.add_argument(
        '--channel', type=int, choices=range(1, 4),
        help='Specify the channel (1, 2, or 3). Required for all operations except general scan.'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Enable verbose output.'
    )

    args = parser.parse_args()

    # Check if a channel-related command is issued without specifying a channel
    if any([args.manage, args.connect, args.disconnect, args.list]) and not args.channel:
        print("Error: --channel is required for manage, connect, disconnect, and list operations.", file=sys.stderr)
        sys.exit(1)

    try:
        channel = 'default' if args.channel is None else str(args.channel)
        bluetooth_manager = BluetoothManager(channel=channel)

        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        if args.manage:
            bluetooth_manager.manage_connections()
            print(f"Bluetooth device management has started on channel {args.channel}.")

        if args.scan:
            devices = bluetooth_manager.discover_devices()
            print("Scanning for Bluetooth devices:")
            for device in devices:
                print(device)

        if args.connect:
            bluetooth_manager.connect_device(args.connect)
            print(f"Attempting to connect to device {args.connect} on channel {args.channel}.")

        if args.disconnect:
            bluetooth_manager.disconnect_all_devices()
            print(f"All devices on channel {args.channel} have been disconnected.")

        if args.list:
            devices = bluetooth_manager.list_connected_devices()
            print(f"Connected devices on channel {args.channel}:")
            for device in devices:
                print(device)

    except BluetoothManagerError as e:
        print(f"Bluetooth Manager Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()