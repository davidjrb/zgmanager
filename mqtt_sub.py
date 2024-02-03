# mqtt_sub.py

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
    print(f"[mqtt_sub.py] Message received on topic {msg.topic}")
    print(f"[mqtt_sub.py] Message payload: {msg.payload.decode()}")
    print(f"[mqtt_sub.py] Writing to file: {output_file_path}")
    with open(output_file_path, 'a') as file:
        file.write(msg.payload.decode() + '\n')

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"[mqtt_sub.py] Connected to MQTT Broker with result code {rc}")
    client.subscribe(userdata['topic'])
    print(f"[mqtt_sub.py] Subscribed to topic: {userdata['topic']}")

if __name__ == "__main__":
    args = parse_arguments()

    client = mqtt.Client(userdata={'topic': args.topic})
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.host, args.port, 60)
    print("[mqtt_sub.py] Starting MQTT loop...")
    client.loop_forever()