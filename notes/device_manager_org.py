# device_manager.py

import subprocess
import csv
import os
import argparse
import time

# Global dictionary to track device counts
device_counts = {
    'gwdevs': {'before': 0, 'after': 0},
    'devInfo': {'before': 0, 'after': 0},
    'unknown': {'before': 0, 'after': 0}
}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Device Manager')
    parser.add_argument('--gateway', type=str, required=True, help='Gateway ID, e.g., zgX')
    parser.add_argument('--remove_unknown', action='store_true', help='Remove unknown devices (default: False)')
    args = parser.parse_args()
    print(f"[device_manager.py] Argument Input: --gateway {args.gateway}")
    if args.remove_unknown:
        print("[device_manager.py] Remove Unknown Devices: Enabled")
    return args

def run_query_gateway(gateway, remove_unknown=False):
    cmd = ['python3', 'query_gateway.py', '--gateway', gateway]
    if remove_unknown:
        cmd.append('--parse_unknown')
        print(f"[device_manager.py] Initiating query_gateway.py with --gateway {gateway} and --parse_unknown")
    else:
        print(f"[device_manager.py] Initiating query_gateway.py with --gateway {gateway}")
    subprocess.run(cmd)

def read_device_list(gateway):
    csv_file_path = f'data/{gateway}/{gateway}_gwdevs.csv'
    print(f"[device_manager.py] Reading CSV: {csv_file_path}")
    devs2query = []
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                devs2query.append(row['friendly_name'])
    except FileNotFoundError:
        print(f"[device_manager.py] The file {csv_file_path} does not exist.")
    return devs2query

def query_devices(gateway, devices):
    for device in devices:
        command = ['python3', 'query_device.py', '--gateway', gateway, '--device', device]
        print(f"[device_manager.py] Running: {' '.join(command)}")
        subprocess.run(command)
        time.sleep(2)  # Pause for 2 seconds before proceeding to the next iteration

def read_and_remove_unknown_devices(gateway):
    csv_file_path = f'data/{gateway}/{gateway}_unknown.csv'
    print(f"[device_manager.py] Reading Unknown Devices CSV: {csv_file_path}")
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                device_id = row['ieeeAddr']  # Assuming ieeeAddr is the appropriate identifier
                remove_device(gateway, device_id)
                time.sleep(1)  # Wait for 1 second after each removal
    except FileNotFoundError:
        print(f"[device_manager.py] The file {csv_file_path} does not exist.")

def remove_device(gateway, device_id):
    gateway_number = gateway.lstrip('zg')
    gateway_ip = f'10.0.0.{gateway_number}'
    topic = "zigbee2mqtt/bridge/request/device/remove"
    message = f'{{"id":"{device_id}", "force": true}}'
    command = ['python3', 'mqtt_pub.py', '--host', gateway_ip, '--topic', topic, '--message', message]
    print(f"[device_manager.py] Removing Device: {device_id}")
    subprocess.run(command)

def count_devices_in_csv(csv_file_path):
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            return sum(1 for row in reader) - 1  # Subtract 1 for the header
    except FileNotFoundError:
        print(f"[device_manager.py] The file {csv_file_path} does not exist.")
        return 0

def update_counts(gateway, file_key):
    csv_file_path = f'data/{gateway}/{gateway}_{file_key}.csv'
    return count_devices_in_csv(csv_file_path)

def print_device_counts_summary():
    print("\nDevices count\n-----------------")
    for key, counts in device_counts.items():
        print(f"{key}.csv\nbefore: {counts['before']} \nafter: {counts['after']}\n")

def append_to_common_index(gateway, device_counts):
    common_csv_path = 'common/zg_index.csv'
    # Ensure the common directory exists
    os.makedirs(os.path.dirname(common_csv_path), exist_ok=True)
    
    # Check if the file exists to decide on writing headers
    write_header = not os.path.exists(common_csv_path)
    
    with open(common_csv_path, 'a', newline='') as csvfile:
        fieldnames = ['gateway', 'gwdevs', 'devInfo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if write_header:
            writer.writeheader()
        
        writer.writerow({
            'gateway': gateway,
            'gwdevs': device_counts['gwdevs']['after'],
            'devInfo': device_counts['devInfo']['after']
        })

def main():
    args = parse_arguments()
    gateway = args.gateway
    # Update initial counts
    for key in device_counts.keys():
        device_counts[key]['before'] = update_counts(gateway, key)

    if args.remove_unknown:
        run_query_gateway(gateway, remove_unknown=True)
        read_and_remove_unknown_devices(gateway)
    else:
        run_query_gateway(gateway)
        devices = read_device_list(gateway)
        query_devices(gateway, devices)

    # Update final counts
    for key in device_counts.keys():
        device_counts[key]['after'] = update_counts(gateway, key)

    # Print summary
    print_device_counts_summary()
    append_to_common_index(gateway, device_counts)

if __name__ == "__main__":
    main()
