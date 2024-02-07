	- [ ] **Issue 1.**: `ieeeAddress` grabbed in appending process

	This is tricky because there is no reference to `ieeeAddress` in color payload

friendly_name,brightness,color,linkquality
0x00212effff0c20a1,84,"{'x': 0.1355, 'y': 0.0399}",255
0x00212effff0c6783,84,"{'x': 0.351, 'y': 0.9847}",255
LAMPI666,100,"{'x': 0.7006, 'y': 0.2993}",255
zg2-1,100,"{'x': 0.7006, 'y': 0.2993}",255




---

- [x] + mqtt_pub.py
- [x] + mqtt_sub.py
- [x] + parse_dev.py
- [x] + parse_gw.py
- [ ] - query_device.py <-- fixes needed:
	- [ ] **Issue 1.**: `ieeeAddress` grabbed in appending process
	- [ ] **Issue 2.**: Each appending instance should be time-stamped with time of query

- [x] + query_gateway.py

- [ ] 1. - device_manager.py --gateway "zgX"
- [ ] 2. - rename.py --gateway "zgX"
- [ ] 3. - zgmanager.py --from "[zgX1]" --to "[zgX2]" --action "device_manager" or "rename"

---



---

# device_manager.py

## --gateway "zgX"

	1. runs `python3 query_gateway.py --gateway zgX` <-- "zgX" arg inherited
		> generates `data/zgX/zgX_gwdevs.csv` <-- contains list of devices

	2. Once `query_gateway.py` process has completed;
		> generates `devs2query` array from freindly_name colum

	3. For every device in `devs2query` run `query_device.py --gateway "zg" --device "[devs2query(n-1)]"`
		> each itteration appends a reachable device to `data/zgX/zgX_devInfo.csv`

---


# rename.py

## --gateway "zgX"

1. Goes through `data/zgX/zgX_devInfo.csv`
	- rename friendly_names from ieeeAdress format to zgX-Y format (if freindly_name == ieeeAddress ... )
	- deletes ieeeAddress duplicates (keeps newest?)
	- update timestamp of devices WHEN row updated

---

# zgmanager.py --from "[zgX1]" --to "[zgX2]" --action "device_manager" or "rename"

	1. Creates range of [from-to] `gws2do` 

	2. For each gateway in `gws2query` run action

---

Needed improvements:
- every node to host program ? ... Executed with flask?