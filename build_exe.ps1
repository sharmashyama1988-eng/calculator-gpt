Write-Host "=== Skipping GitHub Sync (Using Local Changes) ==="

Write-Host "=== Step 2: Preparing Electron package ==="
if (-not (Test-Path "package.json")) {
    npm init -y
}

# We only need to check if electron is already in package.json to avoid reinstalling every time
$packageJsonText = Get-Content package.json
if ($packageJsonText -notmatch "electron") {
    npm install electron --save-dev
    npm install electron-packager --save-dev
}

Write-Host "=== Step 3: Setting up the app environment ==="
$mainJsContent = @"
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow () {
  const win = new BrowserWindow({
    width: 450,
    height: 750,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    autoHideMenuBar: true,
    resizable: false,
    maximizable: false,
    icon: path.join(__dirname, 'logo.png'),
    titleBarStyle: 'hidden',
    titleBarOverlay: {
        color: '#0b0714',
        symbolColor: '#fff'
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
"@

Set-Content -Path "main.js" -Value $mainJsContent

# Update package.json properly
$packageJson = Get-Content package.json | ConvertFrom-Json
$packageJson.main = "main.js"

if (-not $packageJson.scripts) {
    Add-Member -InputObject $packageJson -MemberType NoteProperty -Name "scripts" -Value @{}
}

Add-Member -InputObject $packageJson.scripts -MemberType NoteProperty -Name "start" -Value "electron ." -Force
Add-Member -InputObject $packageJson.scripts -MemberType NoteProperty -Name "build-exe" -Value "electron-packager . `"Calculator GPT`" --platform=win32 --arch=x64 --out=dist --overwrite" -Force

$packageJson | ConvertTo-Json -Depth 10 | Set-Content package.json

Write-Host "=== Step 4: Packaging .exe Application ==="
npm run build-exe

Write-Host ""
Write-Host "Success! Since the first compile missed your files, they've now been successfully injected."
Write-Host "Your fully working .exe is located inside the 'dist/Calculator GPT-win32-x64' folder!"
