import argparse
import sys
from Bluetooth_manager.manager import BluetoothManager, BluetoothManagerError, load_config

def main():
    # Define the command-line arguments
    parser = argparse.ArgumentParser(
        description='CLI tool for managing Bluetooth devices using specified channels.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--manage', action='store_true',
        help='Activate to start managing Bluetooth devices.\nRequires specifying a channel with --channel.'
    )
    parser.add_argument(
        '--scan', action='store_true',
        help='Scan for available Bluetooth devices.\nCan be used with or without specifying a channel.'
    )
    parser.add_argument(
        '--disconnect', action='store_true',
        help='Disconnect all devices on a specified channel.\nRequires specifying a channel with --channel.'
    )
    parser.add_argument(
        '--list', action='store_true',
        help='List all connected devices on a specified channel.\nRequires specifying a channel with --channel.'
    )
    parser.add_argument(
        '--channel', type=int, choices=range(1, 4),
        help='Specify the channel for Bluetooth operations (1, 2, or 3).\nRequired for --manage, --disconnect, and --list.'
    )

    args = parser.parse_args()

    if not any([args.manage, args.scan, args.disconnect, args.list]):
        parser.print_help()
        sys.exit(0)

    try:
        # Load the base configuration
        config = load_config()
        
        if args.channel:
            channel_key = f'channel_{args.channel}'
            if channel_key not in config:
                print(f"Error: No configuration found for channel {args.channel}.", file=sys.stderr)
                sys.exit(1)

        if args.manage:
            if args.channel is None:
                print("Error: --manage requires a channel to be specified.", file=sys.stderr)
                sys.exit(1)
            bluetooth_manager = BluetoothManager(channel=args.channel)
            bluetooth_manager.manage_connections()
            print("Bluetooth device management has started successfully on channel {}.".format(args.channel))

        if args.scan:
            bluetooth_manager = BluetoothManager(channel=args.channel if args.channel else 'default')
            bluetooth_manager.scan_devices()
            print("Scanning for Bluetooth devices has started.")

        if args.disconnect:
            if args.channel is None:
                print("Error: --disconnect requires a channel to be specified.", file=sys.stderr)
                sys.exit(1)
            bluetooth_manager = BluetoothManager(channel=args.channel)
            bluetooth_manager.disconnect_all()
            print("All devices on channel {} have been disconnected.".format(args.channel))

        if args.list:
            if args.channel is None:
                print("Error: --list requires a channel to be specified.", file=sys.stderr)
                sys.exit(1)
            bluetooth_manager = BluetoothManager(channel=args.channel)
            devices = bluetooth_manager.list_connected_devices()
            print("Connected devices on channel {}:".format(args.channel))
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