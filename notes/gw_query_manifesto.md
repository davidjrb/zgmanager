Project tree:

zgmanager/
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
│  └── zg102
│     ├── backups
│     ├── logs
│     ├── zg102_devInfo.csv
│     └── zg102_gwdevs.csv
├── mqtt_pub.py
├── mqtt_sub.py
├── query_device.py
└── query_gateway.py


---

# Scripts:

```bash

## processes/mqtt_pub.py

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
            print("MQTT Publisher Connected to Broker")
        else:
            print(f"Failed to connect to MQTT Broker: Return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print("MQTT Publisher Disconnected from Broker")

    def connect(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()  # Start the loop in a non-blocking way

    def disconnect(self):
        self.client.loop_stop()  # Stop the loop
        self.client.disconnect()  # Disconnect the client

    def publish(self, topic, message):
        self.connect()
        result = self.client.publish(topic, message)
        # Check for successful delivery
        if result[0] == 0:
            print(f"Successfully sent message to topic {topic}")
        else:
            print(f"Failed to send message to topic {topic}")
        self.disconnect()

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

    # Wait for the specified delay
    if args.delay > 0:
        time.sleep(args.delay)

    # Initialize MQTTPublisher
    publisher = MQTTPublisher(args.host, args.port)

    # Publish the message
    publisher.publish(args.topic, args.message)

```

---

```bash

# processes/mqtt_sub.py

import paho.mqtt.client as mqtt

class MQTTSubscriber:
    def __init__(self, host, port=1883):
        self.client = mqtt.Client()
        self.host = host
        self.port = port
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    def start(self, topic, on_message_callback):
        self.client.on_message = on_message_callback
        self.client.connect(self.host, self.port, 60)
        self.client.subscribe(topic)
        self.client.loop_forever()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
```

---

# Desired script behavior:



## query_gateway.py

Execution: 
query_gateway.py --gateway "zgX" --pub_delay [time]
   - time is in seconds

Script starts:

1. from zgX flag arg provided, it determines corresponding:
   - gw_name = zgX
   - ip_address = 10.0.0.X
   - gwdevs_csv = zgmanager/data/zgX/zgX_gwdevs.csv

2. parses field_values from gwdevs_csv:
     friendly_name,lastSeen,ieeeAddr,model

3. initiates external process of mqtt_pub.py --ip_address 10.0.0.X --pub_delay [time] 
   - time arg inherited from previously
   - topic:   "zigbee2mqtt/bridge/config/devices/get"
   - payload: ""

4. start mqtt_sub.py process
   ip_address = 10.0.0.X
   mqttSubTopic = "zigbee2mqtt/bridge/log"

5. verify payload is recieved
   {"message":[{"dateCode":"0x26780700","friendly_name":"Coordinator","ieeeAddr":"0x00212effff099513","lastSeen":1706579789236,"networkAddress":0,"softwareBuildID":"ConBee2/RaspBee2","type":"Coordinator"},{"dateCode":"20220617\u0000","description":"ZigBee Light Link wireless electronic ballast","friendly_name":"0x00212effff0c6783","hardwareVersion":1,"ieeeAddr":"0x00212effff0c6783","lastSeen":1706459000553,"manufacturerID":4405,"manufacturerName":"dresden elektronik\u0000","model":"Mega23M12","modelID":"FLS-PP3\u0000","networkAddress":28319,"powerSource":"Mains (single phase)","softwareBuildID":"0214.201000F6\u0000","type":"Router","vendor":"Dresden Elektronik"},{"dateCode":"20220617\u0000","description":"ZigBee Light Link wireless electronic ballast","friendly_name":"0x00212effff0c20a1","hardwareVersion":1,"ieeeAddr":"0x00212effff0c20a1","lastSeen":1706573709129,"manufacturerID":4405,"manufacturerName":"dresden elektronik\u0000","model":"Mega23M12","modelID":"FLS-PP3\u0000","networkAddress":50742,"powerSource":"Mains (single phase)","softwareBuildID":"0214.201000F6\u0000","type":"Router","vendor":"Dresden Elektronik"},{"dateCode":"20220617\u0000","description":"ZigBee Light Link wireless electronic ballast","friendly_name":"zg2-1","hardwareVersion":1,"ieeeAddr":"0x00212effff0300a4","lastSeen":1706560747300,"manufacturerID":4405,"manufacturerName":"dresden elektronik\u0000","model":"Mega23M12","modelID":"FLS-PP3\u0000","networkAddress":33923,"powerSource":"Mains (single phase)","softwareBuildID":"0214.201000F6\u0000","type":"Router","vendor":"Dresden Elektronik"}],"type":"devices"}

6. terminate mqtt_sub process

7. parse applicable fields and write them to gwdevs_csv in the following way:
   - friendly_name is the unique identifier for every row
   - sorted by friendly_name A-Z
   - when a new friendly_name appears, a new row is created for it
   - if friendly_name already exists cells get overwritten in that row

---

X represents:

- zgX_gwdevs.csv fields: friendly_name,lastSeen,ieeeAddr,model

zgX dirs can vary, all csv's in zgX inherit dir's X

---