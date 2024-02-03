# query_gateway.py 

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
    subprocess.Popen(['python3', 'mqtt_pub.py', '--host', gateway_ip, '--port', '1883', '--topic', topic, '--message', message, '--delay', str(delay)])

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
