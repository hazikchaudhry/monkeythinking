#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if ! command -v uv &> /dev/null; then
    echo "Error: uv was not found."
    echo ""
    echo "Install it with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Then restart your terminal and re-run this script."
    echo "(No uv? Use ./setup-pip.sh instead - it only needs Python.)"
    exit 1
fi

echo "Syncing dependencies (uv will also fetch a matching Python version if needed)..."
uv sync

echo ""
echo "Checking required assets..."
missing=0
for f in models/hand_landmarker.task meme/staring.png meme/pointing.png meme/thinking.png; do
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
echo "Setup complete. To get started:"
echo "  Fill in starter_code.py, then: uv run python starter_code.py"
echo "  Or work through workshop_simple.ipynb in Jupyter."
echo ""
echo "Want to see the finished version? uv run python solutions/solution.py"
echo ""
echo "If the camera window doesn't open: on macOS, allow camera access when prompted"
echo "(or check System Settings > Privacy & Security > Camera), and close apps like"
echo "Zoom/Teams/OBS that may already be holding the webcam."
