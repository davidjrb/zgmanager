

Usage Concept:

```bash
device_manager.py --single "zgX"
```

```bash
zgmanager.py --from "zgX" --to "zgY"
```

for example:
where   X = 101   &   Y = 104   queris >>>   101, 102, 103, 104


//


# device_manager.py

## --single "zgX"

1. query_gateway.py --gateway zgX
	> generates zgX/zgX_gwdevs.csv
	   > contains list of n devices
2. query_ device.py --gateway zgX --device n
	> runs above n iterations in tandem
3. 