# parse_gw.py

import argparse
import json
import csv
import re

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Parse Gateway Data')
    parser.add_argument('--input', type=str, required=True, help='Input file containing MQTT data')
    parser.add_argument('--output', type=str, required=True, help='Output CSV file path')
    return parser.parse_args()

def clean_json(raw_data):
    try:
        # Using regex to extract the first valid JSON object
        match = re.search(r'\{.*\}', raw_data)
        if match:
            print("[parse_gw.py] Cleaned JSON data successfully.")
        else:
            print("[parse_gw.py] No JSON object found.")
        return match.group() if match else None
    except Exception as e:
        print(f"[parse_gw.py] Error cleaning data: {e}")
        return None

# Function to parse and update CSV based on ieeeAddr
def update_csv(input_file, output_csv):
    try:
        with open(input_file, 'r') as file:
            raw_data = file.read().strip()
            print("[parse_gw.py] Reading input file...")

            data = json.loads(raw_data)
            devices = data['message']
            print("[parse_gw.py] JSON data loaded.")

            current_data = {}
            try:
                with open(output_csv, mode='r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Use ieeeAddr as the key
                        current_data[row['ieeeAddr']] = row
                print("[parse_gw.py] Existing CSV data loaded.")
            except FileNotFoundError:
                print(f"[parse_gw.py] CSV file {output_csv} not found. A new file will be created.")

            for device in devices:
                if device.get('model') == 'Mega23M12':
                    ieeeAddr = device.get('ieeeAddr')
                    if ieeeAddr:
                        # Update or add the device by ieeeAddr
                        current_data[ieeeAddr] = {
                            'friendly_name': device.get('friendly_name'),
                            'lastSeen': device.get('lastSeen'),
                            'ieeeAddr': ieeeAddr,
                            'model': device.get('model')
                        }
                        print(f"[parse_gw.py] Device {ieeeAddr} added/updated.")

            with open(output_csv, mode='w', newline='') as file:
                fieldnames = ['friendly_name', 'lastSeen', 'ieeeAddr', 'model']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in sorted(current_data.values(), key=lambda x: x['ieeeAddr']):
                    writer.writerow(row)
                print("[parse_gw.py] CSV file updated.")

    except json.JSONDecodeError as e:
        print(f"[parse_gw.py] Error decoding JSON from input file: {e}")

if __name__ == "__main__":
    args = parse_arguments()
    print("[parse_gw.py] Script started.")
    update_csv(args.input, args.output)
    print("[parse_gw.py] Script finished.")

# [note2self] 
#    Lines that contain devices with matching ieeeAddr names as those present in the input data get replaced in their entirety (all fields) 