Add-Type -AssemblyName System.Drawing
$srcPath = "d:\caculator-gpt\logo.png"
$destPath = "d:\caculator-gpt\logo_256.png"

try {
    $srcImage = [System.Drawing.Image]::FromFile($srcPath)
    $destImage = New-Object System.Drawing.Bitmap(256, 256)
    $graphics = [System.Drawing.Graphics]::FromImage($destImage)
    
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.DrawImage($srcImage, 0, 0, 256, 256)
    
    $destImage.Save($destPath, [System.Drawing.Imaging.ImageFormat]::Png)
    
    $graphics.Dispose()
    $destImage.Dispose()
    $srcImage.Dispose()
    Write-Host "Success! Resized logo to 256x256 at $destPath"
} catch {
    Write-Host "Error: Unable to resize image. $_"
}
