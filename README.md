Tested on Python 3.11
## Setup (Important)

This script requires Python 3.11 for full compatibility.

Check your version:
python --version

If not 3.11, run using:
py -3.11 stroke-timelapse-capture.py

Install dependencies:
py -3.11 -m pip install -r requirements.txt


# Stroke-Based Timelapse Capture

A lightweight Python script that automatically captures screenshots and saves them as sequentially numbered JPG images.

This tool is especially friendly for illustrators who want to create timelapse recordings of their work without recording idle time. It captures frames efficiently with small file sizes (around 60–70 KB each), making it suitable for long-hour drawing sessions.

Tested use case environments include:
- Wacom Mobile Studio Pro 13 Gen 1 by :contentReference[oaicite:0]{index=0}
- RETAS Studio Stylos

Screenshots can later be combined into a video using any external image-to-video converter tool of your choice.


---

## Features
- Capture only when drawing
- Stroke-triggered screenshots
- Auto-pause when drawing app minimized
- Manual pause hotkey
- Optimized JPEG compression
- Sequential filenames:
  Rec_000000.jpg → Rec_000001.jpg

---

## Controls
Key | Action
----|------
F8 | Pause / Resume
ESC | Exit program

---
## Compatibility

This tool is tested and confirmed working on:

Python versions:
- ✅ 3.11 (recommended)
- ⚠ 3.12+ may cause input detection errors
- ❌ 3.13 currently unsupported due to pynput limitations

If you experience crashes or listener errors, install Python 3.11 and run the script using that version.


