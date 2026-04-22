$neuDist = "dist\calculatorgpt"
$electronDist = "dist\Calculator GPT-win32-x64"
$msixDir = "build_msix"

# 1. Detect which build is present
if (Test-Path "$neuDist\calculatorgpt-win_x64.exe") {
    $sourcePath = $neuDist
    $exeName = "calculatorgpt-win_x64.exe"
    Write-Host "Detected Neutralinojs Build (Micro size)!"
} elseif (Test-Path "$electronDist\Calculator GPT.exe") {
    $sourcePath = $electronDist
    $exeName = "Calculator GPT.exe"
    Write-Host "Detected Electron Build (Standard size)!"
} else {
    Write-Host "Error: No build detected. Please run 'neu build' or 'npm run build-exe' first."
    Exit
}

Write-Host "=== Setting up MSIX Hero build directory ==="
if (Test-Path $msixDir) { Remove-Item -Recurse -Force $msixDir }
New-Item -ItemType Directory -Path $msixDir | Out-Null
New-Item -ItemType Directory -Path "$msixDir\Assets" | Out-Null

# 2. Copy application files
Write-Host "1/3. Copying $sourcePath files..."
Copy-Item -Path "$sourcePath\*" -Destination $msixDir -Recurse -Force

# 3. Generating Manifest
Write-Host "2/3. Generating AppxManifest.xml for $exeName..."
$manifestContent = @"
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         IgnorableNamespaces="uap rescap">

  <Identity Name="Technicalamiteducation.caculator-gpt"
            Publisher="CN=3B21D16C-D99E-4486-80B5-89D0B6FCE7CE"
            Version="1.0.7.0"
            ProcessorArchitecture="x64" />

  <Properties>
    <DisplayName>caculator-gpt</DisplayName>
    <PublisherDisplayName>Technical amit (education)</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
  </Properties>

  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.19041.0" />
  </Dependencies>

  <Resources><Resource Language="en-us" /></Resources>

  <Applications>
    <Application Id="CalculatorGPT"
                 Executable="$($exeName)"
                 EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName="caculator-gpt"
                          Description="AI-Powered Natural Language Calculator"
                          BackgroundColor="transparent"
                          Square150x150Logo="Assets\Square150x150Logo.png"
                          Square44x44Logo="Assets\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Assets\Wide310x150Logo.png" />
      </uap:VisualElements>
    </Application>
  </Applications>

  <Capabilities><rescap:Capability Name="runFullTrust" /></Capabilities>
</Package>
"@

Set-Content -Path "$msixDir\AppxManifest.xml" -Value $manifestContent -Encoding UTF8

Write-Host "3/3. Setting actual logo.png for MSIX assets..."
Copy-Item -Path "logo.png" -Destination "$msixDir\Assets\StoreLogo.png" -Force
Copy-Item -Path "logo.png" -Destination "$msixDir\Assets\Square150x150Logo.png" -Force
Copy-Item -Path "logo.png" -Destination "$msixDir\Assets\Square44x44Logo.png" -Force
Copy-Item -Path "logo.png" -Destination "$msixDir\Assets\Wide310x150Logo.png" -Force

Write-Host "Done! MSIX Hero can now use 'build_msix' folder."


Write-Host ""
Write-Host "Done! Your MSIX packager folder 'build_msix' is compiled and ready."
Write-Host "Instructions:"
Write-Host "1. Open MSIX Hero and select 'Pack to MSIX'."
Write-Host "2. Point it straight to your new 'build_msix' folder inside the d:\caculator-gpt workspace."
Write-Host "3. Make sure you use MSIX Hero's Visual Assets generator to automatically replace the placeholders with your logo!"
