Write-Host "=== Environment Check ==="
Write-Host ""
Write-Host "OPENAI_API_KEY:"
$env:OPENAI_API_KEY
Write-Host ""
Write-Host "=== Config File Check ==="
Write-Host ""
if (Test-Path "config.json") {
    Get-Content "config.json" | Write-Host
} else {
    Write-Host "config.json file not found"
}
Write-Host ""
Write-Host "=== Check Complete ==="
