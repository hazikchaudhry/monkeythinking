# Monkey Thinking

Hand gesture detection using MediaPipe and OpenCV — point at the camera to summon a meme.

## Requirements

- [uv](https://docs.astral.sh/uv/) (recommended) — manages Python and dependencies for you, no separate Python install needed
- Or plain Python 3 (tested on 3.13) if you'd rather use pip
- A webcam

## Setup

macOS/Linux:

```bash
./setup.sh
```

Windows (PowerShell):

```powershell
.\setup.ps1
```

This prints a one-line install command if you don't have [uv](https://docs.astral.sh/uv/) yet, then `uv sync`s the pinned dependencies from `pyproject.toml`/`uv.lock` (fetching a matching Python version itself if needed) and checks that the model and meme assets are present.

No uv, or can't install it? Use `./setup-pip.sh` (or `.\setup-pip.ps1` on Windows) instead — same checks, plain `venv` + `pip install -r requirements.txt`.

## Usage

```bash
uv run python main.py
```

Fallback path: `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`), then `python main.py`.

Press 'q' to quit.

Prefer a guided, step-by-step walkthrough? Open `workshop_simple.ipynb` in Jupyter instead. There's also a `starter_code.py` / `solution.py` pair if you'd rather build it yourself in a plain script.

## Features

- Real-time hand landmark detection
- Gesture recognition (pointing)
- Side-by-side meme display
- Supports up to 2 hands simultaneously

## Troubleshooting

- **Camera won't open**: the app tries indexes 0, 1, 2 automatically and prints which one worked. If none open, another app (Zoom/Teams/OBS) may be holding the webcam — close it and retry.
- **macOS camera permission**: the first run triggers a one-time system permission prompt. If you missed it or said no, check System Settings > Privacy & Security > Camera.
- **`ModuleNotFoundError` (pip fallback path only)**: the virtual environment isn't activated — run the `source` / `Activate.ps1` line above first. `uv run` doesn't need this, it handles the environment for you.
- **Windows PowerShell blocks a script**: run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once per terminal session, then retry.
