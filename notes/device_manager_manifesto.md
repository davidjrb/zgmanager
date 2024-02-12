
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
