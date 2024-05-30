let selectedDeviceBtn = null; // Variable to store the selected device
let host_ssid = null; // Variable to store the SSID of the host
let ssid = null; // Variable to store the SSID of wifi environment
let ip = null; // Variable to store the IP address
let gattServer = null; // Variable to store the GATT server

// Get the SSID of the WiFi network
document.addEventListener('DOMContentLoaded', async () => {
  host_ssid = await window.api.getSSID();
});

document.getElementById('bt-scan-btn').addEventListener('click', () => {
  // Change button text
  document.getElementById('bt-scan-btn').innerHTML = 'Scanning...';
  document.getElementById('bt-scan-btn').disabled = true;

  // Send a message to the main process to start scanning for devices
  scanForBluetoothDevices();
});

async function scanForBluetoothDevices() {
  const deviceListElement = document.getElementById('device-list');
  deviceListElement.innerHTML = 'Scanning...'; // Indicate scanning

  const device = await navigator.bluetooth.requestDevice({
    filters: [{
      namePrefix: 'OralEye',
    }],
    optionalServices: ['12345678-1234-5678-1234-56789abcdef0']
  });
  if (device) {
    pairAndConnect(device);
  }
}

window.api.onUpdateDeviceList((deviceList) => {
  const deviceListElement = document.getElementById('device-list');
  deviceListElement.innerHTML = ''; // Clear the list

  deviceList.forEach(device => {
    console.log('Adding Device:', device);
    const listItem = document.createElement('li');
    listItem.classList.add('list-group-item');
    listItem.innerHTML = `
      ${device.deviceName} (ID: ${device.deviceId})
      <button class="btn btn-success btn-sm float-right pair-button" data-device-id="${device.deviceId}">Check Status</button>
    `;

    // Add event listener for the button
    listItem.querySelector('.pair-button').addEventListener('click', (event) => {
      selectedDeviceBtn = event.target;
      const deviceId = event.target.getAttribute('data-device-id');

      // Check the button label on the selected device
      if (selectedDeviceBtn.innerHTML === 'Ready') {
        // Redirect to preview window
        // TODO: implement the preview window
        console.log('Redirecting to preview window');
      } else if (selectedDeviceBtn.innerHTML === 'Check Status') {
        // Send the selected device to the main process
        window.api.sendSelectedDevice(deviceId);
      } else if (selectedDeviceBtn.innerHTML === 'Setup') {
        // Get the host wifi info and share with the device
        window.api.getWiFiInfo().then(wifiInfo => {
          console.log('WiFi Info:', wifiInfo);
          if (wifiInfo) {
            const ssid = wifiInfo.ssid;
            const password = wifiInfo.password;
            console.log('SSID:', ssid);
            console.log('Password:', password);
            // Send the SSID and password to the device
          }
        });
      } else {
        console.log('Invalid button label:', selectedDeviceBtn.innerHTML);
      }
    });
    deviceListElement.appendChild(listItem);
  });
});

function pairAndConnect(device) {
  if (!device) {
    console.log('No device selected');
    return;
  }
  console.log('Selected device name:', device.name);
  console.log('id:', device.id);

  // Update the label of the selected button
  if (selectedDeviceBtn) {
    selectedDeviceBtn.innerHTML = 'Connecting...';
    selectedDeviceBtn.disabled = true;
  }

  // Connect to the GATT Server
  device.gatt.connect().then(server => {
    console.log('Getting Service...');
    gattServer = server;
    return server.getPrimaryService('12345678-1234-5678-1234-56789abcdef0');
  })
    .then(service => {
      return service.getCharacteristic('87654321-4321-6789-4321-56789abcdef0');
    })
    .then(characteristic => {
      console.log('Reading WiFi Characteristic...');
      return characteristic.readValue();
    })
    .then(value => {
      let decoder = new TextDecoder('utf-8');
      let wifiStatus = decoder.decode(value);
      console.log('OralEye Device ', wifiStatus);

      // Check if the device is already connected to WiFi
      // If the device is connected, the return message will be
      //    Connected to SSID, IP: IPv4 IPv6
      // If the device is not connected, the return message will be
      //    Not connected
      const wifiReady = false;
      if (wifiStatus.startsWith('Connected to')) {
        // Parse the SSID and IP address
        const match = wifiStatus.match(/Connected to (.+), IP: (.+)/);
        if (match) {
          ssid = match[1];
          ip = match[2];
          console.log('Connected to:', ssid);
          console.log('IP:', ip);

          if (ssid === host_ssid) {
            // Update the button label
            if (selectedDeviceBtn) {
              selectedDeviceBtn.innerHTML = 'Ready';
              selectedDeviceBtn.disabled = false;
              wifiReady = true;
            }

            // Wifi communication pathway ready. Disconnect bluetooth.
            device.gatt.disconnect();
            gattServer = null;
          } else {
            // Show a warning message
            alert('OralEye device is connected to a different WiFi network: ' + ssid);
          }
        }
        if (!wifiReady) {
          selectedDeviceBtn.innerHTML = 'Setup';
          selectedDeviceBtn.disabled = false;
        }
      }

      // Reset the scan button
      document.getElementById('bt-scan-btn').innerHTML = 'Scan';
      document.getElementById('bt-scan-btn').disabled = false;
    })
    .catch(error => {
      console.error('Error:', error);
      if (device.gatt.connected) {
        device.gatt.disconnect();
      }
    });
}