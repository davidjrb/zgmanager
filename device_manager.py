# device_manager.py

import subprocess
import csv
import os
import argparse
import time
import io
import shutil
from datetime import datetime

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

def read_and_remove_unknown_devices(gateway, remove=False):
    csv_file_path = f'data/{gateway}/{gateway}_unknown.csv'
    print(f"[device_manager.py] Reading Unknown Devices CSV: {csv_file_path}")
    if remove:
        # Perform backup and clear operation if --remove_unknown is used
        backup_and_clear_unknown_csv(gateway)
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                device_id = row['ieeeAddr']
                if remove:
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

def read_common_index():
    common_csv_path = 'common/zg_index.csv'
    index_data = {}
    try:
        with open(common_csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                index_data[row['gateway']] = {'gwdevs': row['gwdevs'], 'devInfo': row['devInfo'], 'unknown': row['unknown']}
    except FileNotFoundError:
        print("[device_manager.py] common/zg_index.csv does not exist. It will be created.")
    return index_data

def has_index_changed(index_data, common_csv_path):
    try:
        with open(common_csv_path, 'r', newline='') as csvfile:
            existing_data = csvfile.read()
        new_data = io.StringIO()
        writer = csv.DictWriter(new_data, fieldnames=['gateway', 'gwdevs', 'devInfo', 'unknown'])
        writer.writeheader()
        for gateway in sorted(index_data.keys()):
            writer.writerow({
                'gateway': gateway,
                **index_data[gateway]
            })
        return existing_data != new_data.getvalue()
    except FileNotFoundError:
        return True

def append_to_common_index(gateway, device_counts):
    common_csv_path = 'common/zg_index.csv'
    backup_dir = 'common/backups/'
    os.makedirs(os.path.dirname(common_csv_path), exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)
    
    index_data = read_common_index()
    index_data[gateway] = {
        'gwdevs': device_counts['gwdevs']['after'],
        'devInfo': device_counts['devInfo']['after'],
        'unknown': device_counts['unknown']['after']
    }
    
    if has_index_changed(index_data, common_csv_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = os.path.join(backup_dir, f'zg_index.csv.{timestamp}')
        shutil.copy(common_csv_path, backup_path)
        
        with open(common_csv_path, 'w', newline='') as csvfile:
            fieldnames = ['gateway', 'gwdevs', 'devInfo', 'unknown']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for gateway in sorted(index_data.keys()):
                writer.writerow({
                    'gateway': gateway,
                    **index_data[gateway]
                })

def main():
    args = parse_arguments()
    gateway = args.gateway

    # Update counts before operations
    for key in device_counts:
        device_counts[key]['before'] = update_counts(gateway, key)

    # Run query_gateway with or without removing unknown devices
    run_query_gateway(gateway, remove_unknown=args.remove_unknown)

    # Conditional to handle unknown devices removal or just query them
    if args.remove_unknown:
        # If removing unknown devices, back up, remove, then query remaining devices
        read_and_remove_unknown_devices(gateway, remove=True)
    else:
        # If not removing, still need to read the list of devices to query
        devices = read_device_list(gateway)
        query_devices(gateway, devices)

    # Update counts after operations
    for key in device_counts:
        device_counts[key]['after'] = update_counts(gateway, key)

    # Display the summary and update common index
    print_device_counts_summary()
    append_to_common_index(gateway, device_counts)

if __name__ == "__main__":
    main()
