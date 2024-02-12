# Quick commands

---

- **Rename (publish)**
```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/config/rename" -m '{"old": "LAMPI0001", "new": "LAMPI666"}'
```

---

## Gateway's devices (get all)

- **Gateway's devices (publish)**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/config/devices/get" -m ""
```

- **Gateway's devices (subscribe)**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/bridge/config/devices"
```

---

## Query device color state

- **Single device color state (publish)**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/device_name/get" -m '{"color": ""}'
```

- **Single device color state (subscribe)**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/device_name"
```

---

# Command Index

[Set Color](#set-color)

[Set Multiple Attributes](#set-multiple-attributes)

[Get Commands](#get-commands)

[Group commands](#group-commands)

[Config](#config)

# Set color:

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4"
```

**Publish:**

- **Red Color**:

   ```bash
   #RED
   mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/set" -m '{"color":{"x":0.7006,"y":0.2993}}'
   ```

- **Green Color**:
  
   ```bash
   #GREEN
   mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/set" -m '{"color":{"x":0.1724,"y":0.7468}}'
   ```

- **Blue Color**:
  
   ```bash
   #BLUE
   mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/set" -m '{"color":{"x":0.1355,"y":0.0399}}'
   ```

- **Yellow Color**:
  
   ```bash
   #YELLOW
   mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/set" -m '{"color":{"x":0.4325,"y":0.5000}}'
   ```

- **Cyan Color**:
  
   ```bash
   #CYAN
   mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/set" -m '{"color":{"x":0.1576,"y":0.2365}}'
   ```

- **Magenta Color**:
  
   ```bash
   #MAGNETA
   mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/set" -m '{"color":{"x":0.3833,"y":0.1591}}'
   ```


[Back to Top](#command-index)

# Set multiple attributes:

### **Set brightness, color, and state for a specific device:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/set" -m '{"brightness": 100, "color": {"x": 0.1724, "y": 0.7468}, "state_rgb": "ON", "state_white": "OFF"}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4"
```

[Back to Top](#command-index)

# Get commands:

### **Get a list of all paired devices:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/config/devices/get" -m ""
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/bridge/log"
```

### **Get the current color of a specific device:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4/get" -m '{"color": ""}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/0x00212effff0300a4"
```

[Back to Top](#command-index)

# Group commands:

### **Set color of group:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/group_name/set" -m '{"color":{"x":0.7006,"y":0.2993}}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/group_name"
```

### **Add a device to a group:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/request/group/members/add" -m '{"group": "alles", "device": "0x00212effff0300a4"}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/bridge/log"
```

### **Remove a device from a group:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/request/group/members/remove" -m '{"group": "alles", "device": "0x00212effff0300a4"}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/bridge/log"
```

[Back to Top](#command-index)

# Config:

### **Rename device:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/config/rename" -m '{"old": "0x00212effff0300a4", "new": "new_name"}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/bridge/log"
```

### **Permit join:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/request/permit_join" -m '{"value": true}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/bridge/log"
```

### **Disable join:**

**Publish:**

```bash
mosquitto_pub -h 10.0.0.2 -t "zigbee2mqtt/bridge/request/permit_join" -m '{"value": false}'
```

**Subscribe:**

```bash
mosquitto_sub -h 10.0.0.2 -t "zigbee2mqtt/bridge/log"
```

[Back to Top](#command-index)