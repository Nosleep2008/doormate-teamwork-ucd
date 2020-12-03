const { app, BrowserWindow, ipcMain } = require('electron')


const mdns = require('mdns');
mdns.Browser.defaultResolverSequence[1] = 'DNSServiceGetAddrInfo' in mdns.dns_sd ? mdns.rst.DNSServiceGetAddrInfo() : mdns.rst.getaddrinfo({families:[4]});

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })
  win.loadFile('index.html');

  ipcMain.on('open-tab', (event, url) => {
    win.loadURL(url) 
  });

  const browser = mdns.createBrowser(mdns.tcp('http'));
  browser.on('serviceUp', service => {
    console.log("service up: ", service);
    win.webContents.send('service', service);
  });
  browser.on('serviceDown', service => {
    console.log("service down: ", service);
  });
  browser.start();
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})
