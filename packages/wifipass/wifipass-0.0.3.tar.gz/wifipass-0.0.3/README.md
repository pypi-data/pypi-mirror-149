# wifipass
A tool to create QR codes to share your wifi credentials.

# Prerequisites
You need to have `python3` and `pip` installed.

# Installing
```
pip install wifipass
```

# Running
```
usage: python -m wifipass [-h] --ssid SSID --pw PW --format {PNG,PDF,BOTH}
                   [--out OUT]

optional arguments:
  -h, --help            show this help message and exit
  --ssid SSID           network name
  --pw PW               network password
  --format {PNG,PDF,BOTH}
  --out OUT             basename for the outputfile(s)
  ```
  For example to generate a pdf version:
  ```
  python -m wifipass --ssid YOUR_SSID_HERE --pw YOUR_PW_HERE --format PDF
  ```
