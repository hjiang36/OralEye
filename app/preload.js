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
  getIPAddress: () => ipcRenderer.invoke('get-ip-address'),
  checkStream: (url) => ipcRenderer.invoke('check-stream', url),
  getLightStatus: (ip) => ipcRenderer.invoke('get-light-status', ip),
  setLightStatus: (ip, lightStates) => ipcRenderer.send('set-light-status', ip, lightStates),
  setStreamingStatus: (ip, status) => ipcRenderer.send('set-streaming-status', ip, status),
});