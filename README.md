
## Roadmap:
---

### 2do High Priority:

**Dependencies:**
- [ ] full upgrade rpi
- [ ] make sure mosquitto is installed on all nodes
- [ ] Conbee2 fw
- [ ] z2m 1.35.1 upgrade
- [ ] Field Work: re-pair as needed

---
Node Progress:
|node |rpi|mqt|CB2|z2m|flw|
|-----|---|---|---|---|---|
| 101 |   |   |   |   |   |
| 102 |   |   |   |   |   |
| 103 |   |   |   |   |   |
| 104 |   |   |   |   |   |
| 105 |   |   |   |   |   |
| 106 |   |   |   |   |   |
| 107 | x | x | x | x | x |
| 108 |   |   |   |   |   |
| 109 |   |   |   |   |   |
| 110 |   |   |   |   |   |
| 111 |   |   |   |   |   |
| 112 |   |   |   |   |   |
| 113 |   |   |   |   |   |
| 114 |   |   |   |   |   |
| 115 |   |   |   |   |   |
| 116 |   |   |   |   |   |
| 117 |   |   |   |   |   |


---

**Coding:**
- [ ] add_to_group (device_manager.py)
- [ ] change_color.py (brightness and fade_time as well)
- [ ] GUI
		1. map
		2. color_picker
---

### 2do Low Priority:

Scripts:
- [ ] zgmanager.py --from "[zgX1]" --to "[zgX2]" --action "device_manager" --dmflags
		1. Creates range of [from-to] `gws2do` 
		2. For each gateway in `gws2query` run action
- [ ] alarms / logging / backups / charts / tables

Subroutines:
- [ ] timestamp csv entries
- [ ] human readible last_seen
- [ ] rename_devices
- [ ] `ieeeAddress` grabbed in devinfo update process

---

**Done:**
- [x] mqtt_pub.py
- [x] mqtt_sub.py
- [x] parse_dev.py
- [x] parse_gw.py
- [x] query_device.py

---

**Directory Structure:**

```bash
zgmanager/
.
│
├── __init__.py
├── dev_json.txt
├── device_manager.py
├── gw_json.txt
├── mqtt_pub.py
├── mqtt_sub.py
├── parse_dev.py
├── parse_gw.py
├── parse_unknown.py
├── query_device.py
├── query_gateway.py
│
├── data
│  ├── copy2all.py
│  ├── devInfo_TEMPLATE.csv
│  ├── dirCreator.py
│  ├── gwdevs_TEMPLATE.csv
│  ├── zg101
│  │  ├── backups
│  │  ├── logs
│  │  ├── zg101_devInfo.csv
│  │  └── zg101_gwdevs.csv
....(more)
│  └── zg117
│     ├── backups
│     ├── logs
│     ├── zg117_devInfo.csv
│     └── zg117_gwdevs.csv
│
└── common
	├── backups
	└── zg_index.csv
```
---

## `device_manager.py`

The `device_manager.py` script manages zigbee2mqtt gateways in the following way:

### Default Operation
```bash
python3 device_manager.py --gateway "zgX"
```
- **Steps**:
  1. Executes `query_gateway.py` to query all devices for gateway.
  2. Reads `data/zgX/zgX_gwdevs.csv` to compile a list of all paired devices.
  3. Queries each device in the list using `query_device.py` to gather their current states.
  4. Updates `data/zgX/zgX_devInfo.csv` with the latest state information for responsive devices.
  5. Reflects the updated total device counts in `common/zg_index.csv`.

### Remove Unknown Devices
```bash
python3 device_manager.py --gateway "zgX" --remove_unknown
```
- **Steps**:
  1. Initiates `query_gateway.py` with the `--parse_unknown` flag to identify unknown devices.
  2. Lists devices for removal from `data/zgX/zgX_unknown.csv`.
  3. Issues MQTT commands to remove each listed device.
  4. Post-removal, updates device counts in `common/zg_index.csv`.

---

## CSV data

- **Argument Parsing** `zgX`: Parsed according to expected subnet and directory structure.

- **Paired Devices** (`zgX_gwdevs.csv`): Lists all devices known to the gateway excluding filtered devices.

- **Unknown Devices** (`zgX_unknown.csv`): Contains devices flagged as unknown during the latest scan.

- **Device States** (`zgX_devInfo.csv`): Records the current state (e.g., brightness, color, link quality) of responsive devices.

- **Gateway Index** (`common/zg_index.csv`): Maintains an updated record of device counts across all gateways, including unknown devices. This file is backed up to `common/backups/` with a timestamp if changes are detected.

---

## Script Expectations
- **zigbee2mqtt**: For managing Zigbee devices.
- **Devices**: Other than "Mega23M12" are flagged "unknown" and removed.
- **`zgX`**: flag is parsed according to expected subnet and directories:
  - directories in .gitignore should be created from template_* folders
  - subnet: 10.0.0.X/24
