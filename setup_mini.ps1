# === Step 1: Install Neutralino CLI ===
Write-Host "Installing Neutralino CLI..."
npm install -g @neutralinojs/neu

# === Step 2: Setup folder structure ===
Write-Host "Creating Neutralino structure..."
if (-not (Test-Path "resources")) {
    New-Item -ItemType Directory -Path "resources"
}

# Copy your actual application files to resources
Copy-Item -Path "index.html" -Destination "resources/index.html" -Force
if (Test-Path "logo.png") {
    Copy-Item -Path "logo.png" -Destination "resources/logo.png" -Force
}

# === Step 3: Create Neutralino Config ===
$neuConfig = @"
{
  "applicationId": "js.neutralino.calculatorgpt",
  "version": "1.0.0",
  "defaultMode": "window",
  "port": 0,
  "documentRoot": "/resources/",
  "url": "/",
  "modes": {
    "window": {
      "title": "Calculator GPT",
      "width": 450,
      "height": 750,
      "minWidth": 450,
      "minHeight": 750,
      "maxWidth": 450,
      "maxHeight": 750,
      "resizable": false,
      "icon": "/resources/logo.png"
    }
  },
  "cli": {
    "binaryName": "CalculatorGPT",
    "binaryVersion": "5.3.0",
    "clientVersion": "5.3.0",
    "distributionPath": "/dist/",
    "resourcesPath": "/resources/",
    "extensionsPath": "/extensions/",
    "clientLibrary": "/resources/neutralino.js"
  },
  "logging": {
    "enabled": false
  }
}
"@

Set-Content -Path "neutralino.config.json" -Value $neuConfig

Write-Host ""
Write-Host "=== Neutralino Setup Ready! ==="
Write-Host "Ab sirf ye commands chalao folder ke andar:"
Write-Host "1. neu update (Binaries download karne ke liye)"
Write-Host "2. neu build (Final <5MB App banane ke liye)"
Write-Host ""
Write-Host "Aapka final app 'dist' folder mein banega jo Electron se 50x chota hoga!"
