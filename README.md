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

Windows: double-click `setup.bat`, or run it from a terminal:

```bat
setup.bat
```

This prints a one-line install command if you don't have [uv](https://docs.astral.sh/uv/) yet, then `uv sync`s the pinned dependencies from `pyproject.toml`/`uv.lock` (fetching a matching Python version itself if needed) and checks that the model and meme assets are present. `setup.bat` just runs `setup.ps1` with PowerShell's script-execution restriction bypassed for that one run, so it works even on a machine where `.ps1` files are blocked by default.

No uv, or can't install it? Use `./setup-pip.sh` (macOS/Linux) or `setup-pip.bat` (Windows) instead — same checks, plain `venv` + `pip install -r requirements.txt`.

## Project Layout

- **Start here**: `starter_code.py` (fill in the blanks) — everything you need to begin is at the top level.
- **`solutions/`**: finished/reference code. `solution.py` is the answer key for `starter_code.py`; `main.py` is an earlier working draft of the same thing; `workshop_simple.ipynb` is the same app as a notebook. You don't need this folder to get started — it's there if you're stuck or want to check your work.

## Usage

Fill in the blanks in `starter_code.py`, then:

```bash
uv run python starter_code.py
```

Want to see the finished version, or check your work against it?

```bash
uv run python solutions/solution.py
```

Or open `solutions/workshop_simple.ipynb` in Jupyter if you'd rather see it as a notebook.

Fallback path (no uv): `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`), then `python starter_code.py` (or `python solutions/solution.py`).

Press 'q' to quit.

## Features

- Real-time hand landmark detection
- Gesture recognition (pointing)
- Side-by-side meme display
- Supports up to 2 hands simultaneously

## Troubleshooting

- **Camera won't open**: the app tries indexes 0, 1, 2 automatically and prints which one worked. If none open, another app (Zoom/Teams/OBS) may be holding the webcam — close it and retry.
- **macOS camera permission**: the first run triggers a one-time system permission prompt. If you missed it or said no, check System Settings > Privacy & Security > Camera.
- **`ModuleNotFoundError` (pip fallback path only)**: the virtual environment isn't activated — run the `source` / `Activate.ps1` line above first. `uv run` doesn't need this, it handles the environment for you.
- **Windows PowerShell blocks a script**: use `setup.bat` / `setup-pip.bat` instead of running the `.ps1` files directly — they bypass this automatically. If you're invoking a `.ps1` directly some other way, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once per terminal session first.
