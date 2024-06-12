const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const os = require('os');
const path = require('path');
const bonjour = require('bonjour')();
var OralEyeApi = require('oral_eye_api');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  let btCallback = null;

  mainWindow.webContents.on('select-bluetooth-device', (event, deviceList, callback) => {
    // Save the callback for later use
    btCallback = callback;

    event.preventDefault();
    // Send the list of devices to the renderer process
    mainWindow.webContents.send('update-device-list', deviceList);
  });

  // Listen for the selected device from the renderer process
  ipcMain.on('bt-device-selected', (event, deviceId) => {
    if (btCallback) {
      btCallback(deviceId);
      btCallback = null;
    }
  });

  mainWindow.loadFile('index.html');
    return mainWindow;

}

// Get SSID for Mac
function getSSIDMac() {
  return new Promise((resolve, reject) => {
    exec("networksetup -getairportnetwork en0", (error, stdout, stderr) => {
      if (error) {
        reject(`Error getting SSID: ${stderr}`);
      } else {
        const match = stdout.match(/Current Wi-Fi Network: (.+)/);
        if (match) {
          resolve(match[1].trim());
        } else {
          reject('SSID not found');
        }
      }
    });
  });
}

// Get WiFi Password for Mac
function getWiFiPasswordMac(ssid) {
  return new Promise((resolve, reject) => {
    exec(`security find-generic-password -D 'AirPort network password' -s 'AirPort' -a '${ssid}' -w`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error getting WiFi password: ${stderr}`);
      } else {
        resolve(stdout.trim());
      }
    });
  });
}

// Get WiFi Information for Mac
async function getWiFiInfoMac() {
  try {
      const ssid = await getSSIDMac();
      const password = await getWiFiPasswordMac(ssid);
      return { ssid, password };
  } catch (error) {
      console.error(error);
      return null;
  }
}

// Get SSID for Windows
function getSSIDWindows() {
  return new Promise((resolve, reject) => {
      exec("netsh wlan show interfaces", (error, stdout, stderr) => {
          if (error) {
              reject(`Error getting SSID: ${stderr}`);
          } else {
              const match = stdout.match(/^\s+SSID\s+:\s+(.+)/m);
              if (match) {
                  resolve(match[1].trim());
              } else {
                  reject('SSID not found');
              }
          }
      });
  });
}

// Get WiFi Password for Windows
function getWiFiPasswordWindows(ssid) {
  return new Promise((resolve, reject) => {
      exec(`netsh wlan show profile name="${ssid}" key=clear`, (error, stdout, stderr) => {
          if (error) {
              reject(`Error getting WiFi password: ${stderr}`);
          } else {
              const match = stdout.match(/^\s+Key Content\s+:\s+(.+)/m);
              if (match) {
                  resolve(match[1].trim());
              } else {
                  reject('Password not found');
              }
          }
      });
  });
}

// Get WiFi Information for Windows
async function getWiFiInfoWindows() {
  try {
      const ssid = await getSSIDWindows();
      const password = await getWiFiPasswordWindows(ssid);
      return { ssid, password };
  } catch (error) {
      console.error(error);
      return null;
  }
}

// Main function to get WiFi info based on OS
async function getWiFiInfo() {
  const osType = os.platform();
  if (osType === 'darwin') {
      return await getWiFiInfoMac();
  } else if (osType === 'win32') {
      return await getWiFiInfoWindows();
  } else {
      throw new Error('Unsupported OS');
  }
}

// Get SSID based on OS
async function getSSID() {
  const osType = os.platform();
  if (osType === 'darwin') {
      return await getSSIDMac();
  } else if (osType === 'win32') {
      return await getSSIDWindows();
  } else {
      throw new Error('Unsupported OS');
  }
}

// Expose the get-wifi-info through IPC
ipcMain.handle('get-wifi-info', async () => {
  const wifiInfo = await getWiFiInfo();
  return wifiInfo;
});

// Expose the get-ssid through IPC
ipcMain.handle('get-ssid', async () => {
  const ssid = await getSSID();
  return ssid;
});

app.commandLine.appendSwitch('enable-web-bluetooth', true);

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('ready', () => {
  const mainWindow = createWindow();

  // Browse for all http services
  bonjour.find({ type: 'http' }, function (service) {
    if (service.name.startsWith('Oral')) {
      console.log('Found service:', service.name);
      console.log('Ip:', service.referer.address);
      // Send the service information to the renderer process if needed
      mainWindow.webContents.send('wifi-device-up', { name: service.name, ip: service.referer.address });

      // Create the API client
      var apiClient = new OralEyeApi.ApiClient(basePath="http://" + service.referer.address + ":8080");

      // Get the device current light information
      // TODO: this is placeholder code for testing. Move / expose this code through ipcMain to renderer in future.
      var lightsApi = new OralEyeApi.LightsApi(apiClient);
      lightsApi.lightsStatusGet((error, data, response) => {
        if (error) {
          console.error('Error:', error);
        } else {
          console.log('Data:', data);
        }
      });
    }

  });
});