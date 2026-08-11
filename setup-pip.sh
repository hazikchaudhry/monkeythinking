#!/usr/bin/env bash
# Fallback setup using plain venv + pip. Prefer ./setup.sh (uv) if you can install uv.
set -e

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but was not found. Install Python 3 and try again."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists, reusing .venv"
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Checking required assets..."
missing=0
for f in hand_landmarker.task meme/staring.png meme/pointing.png meme/thinking.png; do
    if [ ! -f "$f" ]; then
        echo "  MISSING: $f"
        missing=1
    fi
done

if [ "$missing" = "1" ]; then
    echo ""
    echo "Some required files are missing (see above) - pull the latest from git before running."
else
    echo "All required files present."
fi

echo ""
echo "Setup complete. To run it:"
echo "  source .venv/bin/activate"
echo "  python main.py"
echo ""
echo "Or work through workshop_simple.ipynb in Jupyter."
echo ""
echo "If the camera window doesn't open: on macOS, allow camera access when prompted"
echo "(or check System Settings > Privacy & Security > Camera), and close apps like"
echo "Zoom/Teams/OBS that may already be holding the webcam."
