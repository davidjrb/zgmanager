
## mqtt_pub.py

~~~bash
import argparse
import time
import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, host, port=1883):
        self.client = mqtt.Client()
        self.host = host
        self.port = port
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[mqtt_pub.py] MQTT Publisher Connected to Broker")
        else:
            print(f"[mqtt_pub.py] Failed to connect to MQTT Broker: Return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print("[mqtt_pub.py] MQTT Publisher Disconnected from Broker")

    def connect(self):
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()  # Start the loop in a non-blocking way
        except Exception as e:
            print(f"[mqtt_pub.py] Error connecting to MQTT Broker: {e}")

    def disconnect(self):
        self.client.loop_stop()  # Stop the loop
        self.client.disconnect()  # Disconnect the client

    def publish(self, topic, message):
        try:
            self.connect()
            result = self.client.publish(topic, message)
            # Check for successful delivery
            if result[0] == 0:
                print(f"[mqtt_pub.py] Successfully sent message to topic {topic}")
            else:
                print(f"[mqtt_pub.py] Failed to send message to topic {topic}")
            self.disconnect()
        except Exception as e:
            print(f"[mqtt_pub.py] Error publishing message: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='MQTT Publisher Test Script')
    parser.add_argument('--host', type=str, required=True, help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--topic', type=str, required=True, help='MQTT topic to publish to')
    parser.add_argument('--message', type=str, required=True, help='Message to publish')
    parser.add_argument('--delay', type=int, default=0, help='Delay in seconds before publishing')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    print("[mqtt_pub.py] Command-line arguments:")
    print(f"[mqtt_pub.py] Host: {args.host}")
    print(f"[mqtt_pub.py] Port: {args.port}")
    print(f"[mqtt_pub.py] Topic: {args.topic}")
    print(f"[mqtt_pub.py] Message: {args.message}")
    print(f"[mqtt_pub.py] Delay: {args.delay} seconds")

    # Wait for the specified delay
    if args.delay > 0:
        time.sleep(args.delay)

    # Initialize MQTTPublisher
    publisher = MQTTPublisher(args.host, args.port)

    # Publish the message
    publisher.publish(args.topic, args.message)
~~~

~~~bash
python3 mqtt_pub.py --host 10.0.0.2 --topic "zigbee2mqtt/zg2-1/get" --message '{"color": ""}'
~~~
_*note the single-'quotes' when payload contains double-"quotes"_

~~~bash
python3 mqtt_pub.py --host 10.0.0.101 --topic "zigbee2mqtt/bridge/config/devices/get" --message "" --delay 1
~~~
`--delay` --> type=int, required=**False**, default=0   (you don't need to use it)

---------------------------------------------------------------------------------------------

## mqtt_sub.py

~~~bash
import argparse
import paho.mqtt.client as mqtt

# Global variable for output file path
output_file_path = ""

# Parse command line arguments
def parse_arguments():
    global output_file_path
    parser = argparse.ArgumentParser(description='MQTT Subscriber')
    parser.add_argument('--host', type=str, required=True, help='MQTT broker host')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port')
    parser.add_argument('--topic', type=str, required=True, help='MQTT topic to subscribe to')
    parser.add_argument('--output', type=str, required=True, help='Output file for messages')
    args = parser.parse_args()
    output_file_path = args.output
    print(f"Host: {args.host}, Port: {args.port}, Topic: {args.topic}, Output File: {args.output}")
    return args

# Callback for when a message is received
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}")
    print(f"Message payload: {msg.payload.decode()}")
    print(f"Writing to file: {output_file_path}")
    with open(output_file_path, 'a') as file:
        file.write(msg.payload.decode() + '\n')

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(userdata['topic'])
    print(f"Subscribed to topic: {userdata['topic']}")

if __name__ == "__main__":
    args = parse_arguments()

    client = mqtt.Client(userdata={'topic': args.topic})
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.host, args.port, 60)
    print("Starting MQTT loop...")
    client.loop_forever()

~~~
~~~bash
python mqtt_sub.py --host <MQTT_BROKER_HOST> --port <MQTT_BROKER_PORT> --topic <MQTT_TOPIC> --output <OUTPUT_FILE_PATH>
~~~

~~~bash
python3 mqtt_sub.py --host 10.0.0.101 --port 1883 --topic "my/topic" --output output.txt
~~~

----------------------------------------------------------------------------------------------

## parse_dev.py

~~~bash
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
~~~

~~~bash
python parse_dev.py --input <INPUT_JSON_FILE> --output <OUTPUT_CSV_FILE> --device <DEVICE_NAME>
~~~

~~~bash
python parse_dev.py --input input_data.json --output output_data.csv --device my_device
~~~

-----------------------------------------------------------------------------------------------

## parse_gw.py

~~~bash

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
        return match.group() if match else None
    except Exception as e:
        print(f"Error cleaning data: {e}")
        return None

# Function to parse and update CSV
def update_csv(input_file, output_csv):
    try:
        with open(input_file, 'r') as file:
            raw_data = file.read().strip()
            clean_data = clean_json(raw_data)
            if clean_data:
                devices = json.loads(clean_data)['message']

                current_data = {}
                try:
                    with open(output_csv, mode='r', newline='') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            current_data[row['friendly_name']] = row
                except FileNotFoundError:
                    print(f"CSV file {output_csv} not found. A new file will be created.")

                for device in devices:
                    if device.get('model') == 'Mega23M12':  # Filter for 'Mega23M12' model
                        friendly_name = device.get('friendly_name')
                        if friendly_name:
                            current_data[friendly_name] = {
                                'friendly_name': friendly_name,
                                'lastSeen': device.get('lastSeen'),
                                'ieeeAddr': device.get('ieeeAddr'),
                                'model': device.get('model')
                            }

                with open(output_csv, mode='w', newline='') as file:
                    fieldnames = ['friendly_name', 'lastSeen', 'ieeeAddr', 'model']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in sorted(current_data.values(), key=lambda x: x['friendly_name']):
                        writer.writerow(row)

            else:
                print("No valid JSON found in the file.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from input file: {e}")

if __name__ == "__main__":
    args = parse_arguments()
    update_csv(args.input, args.output)

~~~

~~~bash
python parse_gw.py --input <INPUT_MQTT_DATA_FILE> --output <OUTPUT_CSV_FILE>
~~~

~~~bash
python3 parse_dev.py --input input_data.json --output parse_dev_output_data.csv --device device_name
~~~

----------------------------------------------------------------------------------------------

## query_device.py

~~~bash
import argparse
import subprocess
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Query Device')
    parser.add_argument('--gateway', type=str, required=True)
    parser.add_argument('--device', type=str, required=True)
    parser.add_argument('--pub_delay', type=int, default=2)
    parser.add_argument('--timeout', type=int, default=3, help='Timeout in seconds (default: 3)')
    parser.add_argument('--skip_parse', action='store_true')
    return parser.parse_args()

def start_mqtt_publish(gateway_ip, device, delay):
    topic = f"zigbee2mqtt/{device}/get"
    message = '{"color": ""}'
    subprocess.run(['python3', 'mqtt_pub.py', '--host', gateway_ip, '--port', '1883', '--topic', topic, '--message', message, '--delay', str(delay)])

def start_mqtt_subscribe(gateway_ip, device):
    topic = f"zigbee2mqtt/{device}"
    return subprocess.Popen(['python3', 'mqtt_sub.py', '--host', gateway_ip, '--port', '1883', '--topic', topic, '--output', 'dev_json.txt'])

def main():
    args = parse_arguments()
    gateway_ip = f'10.0.0.{args.gateway.lstrip("zg")}'
    output_csv = f'data/{args.gateway}/{args.gateway}_devInfo.csv'

    open('dev_json.txt', 'w').close()

    start_mqtt_publish(gateway_ip, args.device, args.pub_delay)
    mqtt_sub_process = start_mqtt_subscribe(gateway_ip, args.device)

    max_attempts = args.timeout
    attempts = 0
    while True:
        time.sleep(1)
        attempts += 1
        if attempts > max_attempts:
            print(f"Timeout: No device data received after {args.timeout} seconds.")
            break

        with open('dev_json.txt', 'r') as file:
            content = file.read().strip()
            if content:
                if not args.skip_parse:
                    subprocess.run(['python3', 'parse_dev.py', '--input', 'dev_json.txt', '--output', output_csv, '--device', args.device])
                break

    mqtt_sub_process.terminate()

if __name__ == "__main__":
    main()


# python3 query_device.py --gateway "zg2" --device "0x00212efff0a1" --timeout 5
~~~

~~~bash
python3 query_device.py --gateway <GATEWAY_ID> --device <DEVICE_ID> --timeout <TIMEOUT_SECONDS>
~~~

~~~bash
python3 query_device.py --gateway "zg2" --device "0x00212efff0a1" --timeout 5
~~~

-----------------------------------------------------------------------------------------------

## query_gateway.py 

~~~bash

import argparse
import subprocess
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Query Gateway')
    parser.add_argument('--gateway', type=str, required=True, help='Gateway name, e.g., zgX')
    parser.add_argument('--pub_delay', type=int, default=2, help='Delay before publishing in seconds (default: 2)')
    parser.add_argument('--skip_parse', action='store_true', help='Skip parsing CSV in this script (default: False)')
    return parser.parse_args()

def start_mqtt_publish(gateway_ip, delay, topic, message):
    subprocess.run(['python3', 'mqtt_pub.py', '--host', gateway_ip, '--port', '1883', '--topic', topic, '--message', message, '--delay', str(delay)])

def start_mqtt_subscribe(gateway_ip, topic, output_file):
    return subprocess.Popen(['python3', 'mqtt_sub.py', '--host', gateway_ip, '--port', '1883', '--topic', topic, '--output', output_file])

def start_parse_gw(input_file, output_csv):
    subprocess.run(['python3', 'parse_gw.py', '--input', input_file, '--output', output_csv])

def main():
    args = parse_arguments()
    gateway_number = args.gateway.lstrip('zg')
    gateway_ip = f'10.0.0.{gateway_number}'
    csv_file = f'data/{args.gateway}/{args.gateway}_gwdevs.csv'
    output_file = 'gw_json.txt'

    # Clear the gw_json.txt file
    open(output_file, 'w').close()

    # Start MQTT Publish Process
    start_mqtt_publish(gateway_ip, args.pub_delay, 'zigbee2mqtt/bridge/config/devices/get', '')

    # Start MQTT Subscribe Process and keep the process reference
    mqtt_sub_process = start_mqtt_subscribe(gateway_ip, 'zigbee2mqtt/bridge/log', output_file)

    # Wait and read the MQTT Subscriber output file
    max_attempts = 20
    attempts = 0
    while True:
        time.sleep(1)
        attempts += 1
        if attempts > max_attempts:
            print("Timeout: No MQTT messages received.")
            break

        with open(output_file, 'r') as file:
            content = file.read().strip()
            if content:  # Check if file is not empty
                if not args.skip_parse:
                    start_parse_gw(output_file, csv_file)
                break

    # Terminate the mqtt_sub.py process to stop appending to the file
    mqtt_sub_process.terminate()

if __name__ == "__main__":
    main()
~~~

~~~bash
python3 query_gateway.py --gateway <GATEWAY_NAME> --pub_delay <DELAY_SECONDS>
~~~

~~~bash
python3 query_gateway.py --gateway "zg2" --pub_delay 3
~~~

-----------------------------------------------------------------------------------------------


## Tree

~~~bash
djeims@Udell ~/g/d/zgmanager (main) [SIGINT]> eza --tree
.
├── __init__.py
├── data
│  ├── copy2all.py
│  ├── devInfo_TEMPLATE.csv
│  ├── dirCreator.py
│  ├── gwdevs_TEMPLATE.csv
│  ├── zg2
│  │  ├── backups
│  │  ├── logs
│  │  ├── zg2_devInfo.csv
│  │  └── zg2_gwdevs.csv
│  ├── zg101
│  │  ├── backups
│  │  ├── logs
│  │  ├── zg101_devInfo.csv
│  │  └── zg101_gwdevs.csv
│  ├── zg102
│  │  ├── backups
│  │  ├── logs
│  │  ├── zg102_devInfo.csv
│  │  └── zg102_gwdevs.csv
....(more)
│  ├── zg116
│  │  ├── backups
│  │  ├── logs
│  │  ├── zg116_devInfo.csv
│  │  └── zg116_gwdevs.csv
│  └── zg117
│     ├── backups
│     ├── logs
│     ├── zg117_devInfo.csv
│     └── zg117_gwdevs.csv
├── dev_json.txt
├── gw_json.txt
├── mqtt_output.txt
├── mqtt_pub.py
├── mqtt_sub.py
├── parse_dev.py
├── parse_gw.py
├── query_device.py
├── query_gateway.py
└── test_output.txt
~~~

----------------------------------------------------------------------------------------------

