# parse_dev.py

import argparse
import json
import csv

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parse Device Data')
    parser.add_argument('--input', type=str, required=True, help='Input JSON file')
    parser.add_argument('--output', type=str, required=True, help='Output CSV file path')
    parser.add_argument('--device', type=str, required=True, help='Device name')
    return parser.parse_args()

def update_csv(input_file, output_csv, device_name):
    try:
        with open(input_file, 'r') as file:
            data = json.loads(file.read().strip())

        current_data = {}
        try:
            with open(output_csv, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    current_data[row['friendly_name']] = row
        except FileNotFoundError:
            print(f"CSV file {output_csv} not found. Creating a new file.")

        # Extract relevant data
        data_entry = {
            'friendly_name': device_name,
            'brightness': data.get('brightness', ''),
            'color': data.get('color', ''),
            'linkquality': data.get('linkquality', '')
        }
        current_data[device_name] = data_entry

        # Write updated data back to CSV
        with open(output_csv, mode='w', newline='') as file:
            fieldnames = ['friendly_name', 'brightness', 'color', 'linkquality']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in sorted(current_data.values(), key=lambda x: x['friendly_name']):
                writer.writerow(row)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from input file: {e}")

if __name__ == "__main__":
    args = parse_arguments()
    update_csv(args.input, args.output, args.device)
