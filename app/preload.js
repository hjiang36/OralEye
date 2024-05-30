const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  onUpdateDeviceList: (callback) => {
    ipcRenderer.on('update-device-list', (event, deviceList) => {
      console.log('Received device list:', deviceList);
      callback(deviceList);
    });
  },
  sendSelectedDevice: (deviceId) => {
    ipcRenderer.send('bt-device-selected', deviceId);
  },
  getWiFiInfo: () => ipcRenderer.invoke('get-wifi-info'),
  getSSID: () => ipcRenderer.invoke('get-ssid'),
});