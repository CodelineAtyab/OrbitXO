# Route Manager (FastAPI)

A simple FastAPI web UI to view, add, and remove source-destination route pairs.
Routes are stored in a local `config.json` file.

## Quick Start (VS Code friendly)

1) **Create & activate a virtual environment** (Windows PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2) **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3) **Run the app**
   ```bash
   uvicorn main:app --reload
   ```

4) Open your browser at: **http://127.0.0.1:8000/**

## What it does
- Shows your current routes (from `config.json`)
- Lets you add new routes (with basic validation)
- Lets you delete routes
- Saves all changes back to `config.json`

## Notes
- "Current estimate" is a placeholder column to be filled later if you connect a travel-time API.
- Config file path can be changed via `CONFIG_PATH` in `main.py`.
