const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const path = require('path');
const bonjour = require('bonjour')();

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

// Get SSID
function getSSID() {
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

// Get WiFi Password
function getWiFiPassword(ssid) {
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

// Function to get WiFi information
async function getWiFiInfo() {
  try {
    const ssid = await getSSID();
    const password = await getWiFiPassword(ssid);
    return { ssid, password };
  } catch (error) {
    console.error(error);
    return null;
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
    }
    
  });
});