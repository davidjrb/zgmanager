import argparse
import subprocess
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description='Send commands to RGB lamps, list available colors, set color by hex, or adjust brightness.')
    parser.add_argument('--gateway', help='Gateway ID (e.g., zg2, zg107). Required for setting values.')
    parser.add_argument('--color', help='Color to set (e.g., RED, BLUE). Optional.')
    parser.add_argument('--hex', help='Hex color value to set (e.g., #547CFF). Optional.')
    parser.add_argument('--brightness', type=int, help='Brightness level to set (0-100). Optional.')
    parser.add_argument('--list', action='store_true', help='List available colors and exit.')
    return parser.parse_args()

def find_color_values(color, filename='colors.md'):
    if not color:
        return None, None  # No color specified, return None
    
    with open(filename, 'r') as file:
        content = file.read()
    
    pattern = rf'#{color}.*?x":([0-9.]+),"y":([0-9.]+)'
    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1), match.group(2)  # Return x, y values
    else:
        raise ValueError(f'Color {color} not found in {filename}')

def list_available_colors(filename='colors.md'):
    with open(filename, 'r') as file:
        content = file.read()
    
    matches = re.findall(r'^#([A-Z]+)$', content, re.IGNORECASE | re.MULTILINE)
    
    if matches:
        print("Available colors:")
        for color in matches:
            print(color)
    else:
        print("No colors found. Please check the format of your colors.md file.")

def construct_and_execute_command(gateway, color=None, hex_value=None, brightness=None):
    if not gateway:
        print('Gateway ID is required for setting values.')
        return
    
    subnet = re.search(r'(\d+)$', gateway)
    if not subnet:
        print('Invalid gateway format. Expected zg followed by numbers.')
        return
    
    ip_address = f'10.0.0.{subnet.group()}'
    
    message_parts = []
    if color:
        x, y = find_color_values(color)
        message_parts.append(f'"color":{{"x":{x},"y":{y}}}')
    if hex_value:
        message_parts.append(f'"color":{{"hex":"{hex_value}"}}')
    if brightness is not None:  # Check if brightness has been specified
        message_parts.append(f'"brightness":{brightness}')
    
    if message_parts:
        message = '{' + ','.join(message_parts) + '}'
        command = f'python3 mqtt_pub.py --host {ip_address} --topic "zigbee2mqtt/alles/set" --message \'{message}\''
        subprocess.run(command, shell=True)
    else:
        print("No valid settings specified. Please include color, hex, and/or brightness.")

if __name__ == '__main__':
    args = parse_arguments()
    
    if args.list:
        list_available_colors()
    elif args.gateway:
        construct_and_execute_command(args.gateway, args.color, args.hex, args.brightness)
    else:
        print("Please specify a gateway ID with --gateway for setting values, or use --list to list available colors.")
