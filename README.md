# OralEye
OralEye prototype software using Raspberry Pi device

This repository contains code for both device side (under [rpi](https://github.com/hjiang36/OralEye/tree/main/rpi) folder) and host side (under [app](https://github.com/hjiang36/OralEye/tree/main/app) folder) control software.

## Getting Started
This device describes how to setup host and device environmnet for developers. Users are strongly recommended to use pre-built relaese binaries (link to be added).

### Device Setup
The device should be configured properly and no special setup steps required. The following steps would only be needed if started with vanilla raspberry pi system.

* **Boot up** the device with keyboard / mouse and monitor.
* **Download** the release zip / tar ball from this repo and uncompress it.
* **Run** `sudo make rpi-setup` from the root of uncompressed repo folder.

All files and settings should be applied. The device will be rebooted and the device is ready to be used.

### Host Setup
For user, we recommend download the app executable in release tag. Here we describe the developer setup to build and run from source code.

* **Install** [node & npm](https://nodejs.org/en/download/package-manager)
* **Run** `npm install` to install all dependencies libraries
* **Run** `make api` to generate API SDK if needed.
* **Run** `npm start` to start the host side application

### API Stub & Client SDK Generation
The OpenAPI definition can be found in `openapi.yaml` file. It can be visually edited with [swagger editor](https://editor.swagger.io/) or any other REST / OpenAPI editing tools.

If changes are made to the `openapi.yaml`, both API stub on Raspberry Pi and client SDK needs to be updated. We use `openapi-generator-cli` to auto-generate the code for stub and SDK, which can be installed using following command. `sudo` may be needed depending on system.

```sh
npm install @openapitools/openapi-generator-cli -g
```
Regeneration can be done with
```sh
make api
```
The corresponding code should be generated to be under `app/api` and `rpi/server` folder.

To run the server code on Raspberry pi, install all depencies with `pip install -r requirements.txt` in `OralEye/rpi/server` folder.
And run the server with `python -m openapi_server` to start the server. The server will be auto-started upon bootup. In development build, we can run this manually.
If code update is made to the `openapi_server`, it is recommended to re-run `pip install --force-reinstall .` from the `OralEye/rpi/server` folder to ensure the latest updates are taking effects.

Once the server is running, the SwaggerUI / API interface can be found at `<IP>:8080/ui`.

## Core Function Manual
### Discovery & Pairing
The OralEye devices are configured to be discoverable through both Wifi and Bluetooth. Wifi discovery is done through mDNS protocol and used for discovery of devices that already on same local network with the host. Bluetooth discover is used for first time pairing, device setup and troubleshooting.


### Streaming

### Camera Control

### Capture

## Troubleshoot

