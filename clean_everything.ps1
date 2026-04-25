# === CRITICAL CLEANUP SCRIPT ===
Write-Host "Cleaning up massive build folders..." -ForegroundColor Yellow

$foldersToDelete = @("dist", "build_msix", "out")

foreach ($folder in $foldersToDelete) {
    if (Test-Path $folder) {
        Write-Host "Deleting $folder..."
        Remove-Item -Recurse -Force $folder -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "Cleanup Done! Your folder size should be back to normal (just source code)." -ForegroundColor Green
Write-Host "Now you can run '.\setup_mini.ps1' then 'neu update' and 'neu build' for the small version."
