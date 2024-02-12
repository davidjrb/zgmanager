

---

- [x] + mqtt_pub.py
- [x] + mqtt_sub.py
- [x] + parse_dev.py
- [x] + parse_gw.py
- [x] + query_device.py
	- [ ] 
	- [ ] **Issue 1.**: 
	- [ ] **Issue 2.**: 
	- [ ] **Issue 3.**: `ieeeAddress` grabbed in devinfo update process
	- [ ] **Issue 4.**: Each csv instance should be time-stamped with time of update
	- [ ] **Issue 5.**: --rename flag (maybe?)
- [x] + query_gateway.py

- [ ] - add_to_group.py

- [ ] - rename.py --gateway "zgX"

- [ ] - zgmanager.py --from "[zgX1]" --to "[zgX2]" --action "device_manager" or "rename"

- [ ] - zigbee2mqtt needs to be updated to 1.35.1 on all gateways or (if all else fails) reversed to `10. Nov 2023` version
	- https://github.com/Koenkk/zigbee2mqtt/releases

- [ ] - ConbeeII fw needs upgrade (see dresden-elektronik.md)

- [ ] - backup

---

ideas:


1. Goes through `data/zgX/zgX_devInfo.csv`
	- rename friendly_names from ieeeAdress format to zgX-Y format (if freindly_name == ieeeAddress ... )
	- deletes ieeeAddress duplicates (keeps newest?)
	- update timestamp of devices WHEN row updated

---

# zgmanager.py --from "[zgX1]" --to "[zgX2]" --action "device_manager" or "rename"

	1. Creates range of [from-to] `gws2do` 

	2. For each gateway in `gws2query` run action

---

# add_to_group.py


---

Needed improvements:
- every node to host program ? ... Executed with flask?