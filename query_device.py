# query_device.py

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
    subprocess.Popen(['python3', 'mqtt_pub.py', '--host', gateway_ip, '--port', '1883', '--topic', topic, '--message', message, '--delay', str(delay)])

def start_mqtt_subscribe(gateway_ip, device):
    topic = f"zigbee2mqtt/{device}"
    return subprocess.Popen(['python3', 'mqtt_sub.py', '--host', gateway_ip, '--port', '1883', '--topic', topic, '--output', 'dev_json.txt'])

def main():
    args = parse_arguments()
    gateway_ip = f'10.0.0.{args.gateway.lstrip("zg")}'
    output_csv = f'data/{args.gateway}/{args.gateway}_devInfo.csv'

# 1. it creates (and therefore overwrites) an empty 'dev_json.txt' file
    open('dev_json.txt', 'w').close()

# 2. starts the unsupervised subprocess of 'mqtt_pub.py' (pull pin and throw)
    start_mqtt_publish(gateway_ip, args.device, args.pub_delay)

# 3. listens for a response from said device
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

# 4. if 'content' (= it's not empty anymore)
            if content:
# 5. If no '--skip_parse' argument provided, proceed with parsing
                if not args.skip_parse:
                    subprocess.run(['python3', 'parse_dev.py', '--input', 'dev_json.txt', '--output', output_csv, '--device', args.device])
# 6. break out of loop because of #4.
                break
# 7. stop the mqtt_sub-routine and exit
    mqtt_sub_process.terminate()

if __name__ == "__main__":
    main()


# python3 query_device.py --gateway "zg2" --device "0x00212efff0a1" --timeout 5
