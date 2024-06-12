const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  onUpdateBtDeviceList: (callback) => {
    ipcRenderer.on('update-device-list', (event, deviceList) => {
      console.log('Received device list:', deviceList);
      callback(deviceList);
    });
  },
  onUpdateWifiDeviceList: (callback) => {
    ipcRenderer.on('wifi-device-up', (event, deviceList) => {
      callback(deviceList);
    });
  },
  sendSelectedBtDevice: (deviceId) => {
    ipcRenderer.send('bt-device-selected', deviceId);
  },
  getWiFiInfo: () => ipcRenderer.invoke('get-wifi-info'),
  getSSID: () => ipcRenderer.invoke('get-ssid'),
});