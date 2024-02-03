# mqtt_pub.py

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
