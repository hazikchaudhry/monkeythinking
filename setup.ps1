$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: uv was not found."
    Write-Host ""
    Write-Host "Install it with (PowerShell):"
    Write-Host '  powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"'
    Write-Host ""
    Write-Host "Then restart your terminal and re-run this script."
    Write-Host "(No uv? Use .\setup-pip.ps1 instead - it only needs Python.)"
    exit 1
}

Write-Host "Syncing dependencies (uv will also fetch a matching Python version if needed)..."
uv sync

Write-Host ""
Write-Host "Checking required assets..."
$missing = $false
foreach ($f in @("hand_landmarker.task", "meme\staring.png", "meme\pointing.png", "meme\thinking.png")) {
    if (-not (Test-Path $f)) {
        Write-Host "  MISSING: $f"
        $missing = $true
    }
}

if ($missing) {
    Write-Host ""
    Write-Host "Some required files are missing (see above) - pull the latest from git before running."
} else {
    Write-Host "All required files present."
}

Write-Host ""
Write-Host "Setup complete. To run it:"
Write-Host "  uv run python main.py"
Write-Host ""
Write-Host "Or work through workshop_simple.ipynb in Jupyter."
Write-Host ""
Write-Host "If PowerShell blocks script execution, run once per terminal session:"
Write-Host "  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
Write-Host ""
Write-Host "If the camera window doesn't open: close apps like Zoom/Teams/OBS that may"
Write-Host "already be holding the webcam, and check Settings > Privacy & Security > Camera"
Write-Host "to make sure desktop apps are allowed to use it."
