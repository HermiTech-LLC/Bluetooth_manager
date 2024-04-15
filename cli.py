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
        help='Activate to start managing Bluetooth devices. Requires specifying a channel with --channel.'
    )
    parser.add_argument(
        '--scan', action='store_true',
        help='Scan for available Bluetooth devices. Can be used with or without specifying a channel.'
    )
    parser.add_argument(
        '--disconnect', action='store_true',
        help='Disconnect all devices on a specified channel. Requires specifying a channel with --channel.'
    )
    parser.add_argument(
        '--list', action='store_true',
        help='List all connected devices on a specified channel. Requires specifying a channel with --channel.'
    )
    parser.add_argument(
        '--channel', type=int, choices=range(1, 4),
        help='Specify the channel for Bluetooth operations (1, 2, or 3). Required for --manage, --disconnect, and --list.'
    )

    args = parser.parse_args()

    if not any([args.manage, args.scan, args.disconnect, args.list]):
        parser.print_help()
        sys.exit(0)

    try:
        channel = 'default' if args.channel is None else str(args.channel)
        bluetooth_manager = BluetoothManager(channel=channel)

        if args.manage:
            if not args.channel:
                print("Error: --manage requires a channel to be specified.", file=sys.stderr)
                sys.exit(1)
            bluetooth_manager.manage_connections()
            print(f"Bluetooth device management has started successfully on channel {args.channel}.")

        if args.scan:
            devices = bluetooth_manager.discover_devices()
            print("Scanning for Bluetooth devices has started:")
            for device in devices:
                print(device)

        if args.disconnect:
            if not args.channel:
                print("Error: --disconnect requires a channel to be specified.", file=sys.stderr)
                sys.exit(1)
            bluetooth_manager.disconnect_all_devices()
            print(f"All devices on channel {args.channel} have been disconnected.")

        if args.list:
            if not args.channel:
                print("Error: --list requires a channel to be specified.", file=sys.stderr)
                sys.exit(1)
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