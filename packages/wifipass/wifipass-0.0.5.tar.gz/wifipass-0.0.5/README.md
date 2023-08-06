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
usage: python -m wifipass [-h] [--ssid SSID] [--pw PW] [--out OUT]

optional arguments:
  -h, --help            show this help message and exit
  --ssid SSID           network name
  --pw PW               network password
  --out OUT             output filename
  ```
  For example to generate a pdf version:
  ```
  python -m wifipass --ssid YOUR_SSID_HERE --pw YOUR_PW_HERE --out qr.pdf
  ```
