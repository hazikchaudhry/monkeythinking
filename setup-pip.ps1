# Fallback setup using plain venv + pip. Prefer .\setup.ps1 (uv) if you can install uv.
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: python was not found. Install Python 3 from python.org and try again."
    Write-Host "(If typing 'python' opens the Microsoft Store, Python isn't actually installed yet.)"
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host "Virtual environment already exists, reusing .venv"
}

& ".venv\Scripts\Activate.ps1"

Write-Host "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "Checking required assets..."
$missing = $false
foreach ($f in @("models\hand_landmarker.task", "meme\staring.png", "meme\pointing.png", "meme\thinking.png")) {
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
Write-Host "Setup complete. To get started:"
Write-Host "  .venv\Scripts\Activate.ps1"
Write-Host "  Fill in starter_code.py, then: python starter_code.py"
Write-Host "  Or work through workshop_simple.ipynb in Jupyter."
Write-Host ""
Write-Host "Want to see the finished version? python solutions/solution.py"
Write-Host ""
Write-Host "If PowerShell blocks script execution, run once per terminal session:"
Write-Host "  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
Write-Host ""
Write-Host "If the camera window doesn't open: close apps like Zoom/Teams/OBS that may"
Write-Host "already be holding the webcam, and check Settings > Privacy & Security > Camera"
Write-Host "to make sure desktop apps are allowed to use it."
