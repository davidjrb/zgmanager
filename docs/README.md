
## Roadmap:
---

### 2do High Priority:

**Dependencies:**
- [ ] make sure mosquitto is installed on all nodes
- [ ] Conbee2 fw
- [ ] z2m 1.35.1 upgrade
- [ ] Field Work: re-pair as needed

---
Node Progress:
|node |mqt|CB2|z2m|flw|
|-----|---|---|---|---|
| 101 |   |   |   |   |
| 102 |   |   |   |   |
| 103 |   |   |   |   |
| 104 |   |   |   |   |
| 105 |   |   |   |   |
| 106 |   |   |   |   |
| 107 | x | x | x | x |
| 108 |   |   |   |   |
| 109 |   |   |   |   |
| 110 |   |   |   |   |
| 111 |   |   |   |   |
| 112 |   |   |   |   |
| 113 |   |   |   |   |
| 114 |   |   |   |   |
| 115 |   |   |   |   |
| 116 |   |   |   |   |
| 117 |   |   |   |   |


---

**Coding:**
- ! [ ] add_to_group (device_manager.py)
- ! [ ] change_color.py (brightness and fade_time as well)
- ! [ ] GUI
		1. map
		2. color_picker
---

### 2do Low Priority:

Scripts:
- ? [ ] zgmanager.py --from "[zgX1]" --to "[zgX2]" --action "device_manager" --dmflags
		1. Creates range of [from-to] `gws2do` 
		2. For each gateway in `gws2query` run action
- ? [ ] alarms / logging / backups / charts / tables

Subroutines:
- ? [ ] timestamp csv entries
- ? [ ] human readible last_seen
- ? [ ] rename_devices
- ? [ ] `ieeeAddress` grabbed in devinfo update process

---

**Done:**
- ! [x] mqtt_pub.py
- ! [x] mqtt_sub.py
- ! [x] parse_dev.py
- ! [x] parse_gw.py
- ! [x] query_device.py

---

**Directory Structure:**

zgmanager/
~/zgmanager (main) > eza --tree
.
│
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
└── query_gateway.py