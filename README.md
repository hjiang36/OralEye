# OralEye
OralEye prototype software using Raspberry Pi device

This repository contains code for both device side (under [rpi](https://github.com/hjiang36/OralEye/tree/main/rpi) folder) and host side (under [app](https://github.com/hjiang36/OralEye/tree/main/app) folder) control software.

## Getting Started
### Device Setup
The device should be configured properly and no special setup steps required. The following steps would only be needed if started with vanilla raspberry pi system.

* **Boot up** the device with keyboard / mouse and monitor.
* **Download** the release zip / tar ball from this repo and uncompress it.
* **Run** `sudo make rpi-setup` from the root of uncompressed repo folder.

All files and settings should be applied. The device will be rebooted and the device is ready to be used.

### Host Developer Setup
For user, we recommend download the app executable in release tag. Here we describe the developer setup to build and run from source code.

* **Install** [node & npm](https://nodejs.org/en/download/package-manager)
* **Run** `npm install` to install all dependencies libraries
* **Run** `npm start` to start the host side application


## Device Control
### Pairing & Configuration

### Streaming

### Camera Control

### Capture

## Troubleshoot