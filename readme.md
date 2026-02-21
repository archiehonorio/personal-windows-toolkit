# 🧰 Personal Windows Toolkit

Hey! I'm just someone who loves editing videos, playing games, and finding ways to make everyday computer tasks less painful. I built these scripts for myself — to save time, free up disk space, stay in Roblox without getting kicked, and handle all the boring file conversion stuff that comes with video editing as a hobby.

I'm sharing them on GitHub because someone out there probably needs the exact same thing. No fancy GUI, no bloated software — just Python scripts you drop and run. Hope it helps! 🙌

---

## 📦 What's Inside

| Tool | Description |
|------|-------------|
| [`converter-pdf-word.py`](#-pdf--word-converter) | Convert PDF ↔ Word automatically |
| [`converter-audiofile.py`](#-audio--video-format-converter) | Convert audio/video to any format via FFmpeg |
| [`vids-download.py`](#-batch-video-downloader) | Download videos from YouTube, TikTok, Instagram, Facebook & more |
| [`find_large_files.py`](#-large-file-finder) | Scan a drive and list the biggest files eating your storage |
| [`anti-afk-roblox.py`](#-roblox-anti-afk) | Stay active in Roblox so you don't get kicked while AFK |

---

## 📄 PDF ↔ Word Converter

When you work with a lot of documents, switching between PDF and Word gets tedious fast. This script detects the file type and converts in the right direction automatically — no flags, no options, no thinking required.

### Setup

```bash
pip install python-docx docx2pdf pdf2docx
```

### Folder Structure

```
📁 your-folder/
├── converter.py
├── FileConvert/      ← drop your files here
└── OutputFile/       ← converted files appear here
```

> Both folders are created automatically on first run.

### Usage

```bash
python converter.py
```

Drop any `.pdf`, `.doc`, or `.docx` files into `FileConvert/` and run the script. It detects the format and converts automatically:

- `.docx` / `.doc` → **PDF**
- `.pdf` → **Word (.docx)**

Supports **batch conversion** — drop multiple files and they all get converted in one run.

### Example Output

```
====================================================
       📁  PDF ↔ Word Batch Converter
====================================================
  Input  folder : /your-folder/FileConvert
  Output folder : /your-folder/OutputFile
====================================================

  Found 2 file(s) to convert...

📄  report.docx
   🔄  Word → PDF
   ✅  Saved → OutputFile/report.pdf

📄  invoice.pdf
   🔄  PDF → Word
   ✅  Saved → OutputFile/invoice.docx

====================================================
  ✔  2 converted   ✘  0 failed
====================================================
```

---

## 🎧 Audio / Video Format Converter

As a video editor, I constantly need to convert between formats — extracting audio from footage, converting clips for different platforms, preparing voice samples for AI tools. This handles all of it from the terminal with a simple menu.

### Requirements

- [FFmpeg](https://ffmpeg.org/download.html) — must be installed and added to PATH

### Folder Structure

```
📁 your-folder/
├── converter_audio.py
├── ScriptsConvert/    ← drop your audio/video files here
└── TestModel/         ← converted files appear here
```

### Usage

```bash
python converter_audio.py
```

Drop your files into `ScriptsConvert/` and run. You'll be shown a menu to choose the output format:

```
──────────────────────────────────────────────────────
  Choose output format:

  ── Audio ──────────────────────────────────────────
  [ 1]  WAV  — 22050 Hz mono 16-bit  (XTTS / TTS reference)
  [ 2]  WAV  — 44100 Hz stereo 16-bit (standard CD quality)
  [ 3]  MP3  — 192 kbps stereo
  [ 4]  MP3  — 320 kbps stereo (high quality)
  [ 5]  AAC  — 192 kbps (iTunes / mobile friendly)
  [ 6]  FLAC — Lossless compressed audio
  [ 7]  OGG  — Vorbis ~192 kbps
  [ 8]  OPUS — 128 kbps (best compression / quality ratio)

  ── Extract Audio from Video ───────────────────────
  [ 9]  MP3  — Extract audio from video (192 kbps)
  [10]  WAV  — Extract audio from video (44100 Hz stereo)

  ── Video ──────────────────────────────────────────
  [11]  MP4  — H.264 video, AAC audio (universal)
  [12]  MP4  — High quality H.264 (CRF 18)
  [13]  MKV  — H.264 video, copy audio streams
  [14]  WEBM — VP9 video (web optimized)
```

### Supported Input Formats

| Type | Formats |
|------|---------|
| Audio | `.mp3` `.m4a` `.aac` `.ogg` `.flac` `.wav` `.wma` `.opus` `.aiff` |
| Video | `.mp4` `.mkv` `.mov` `.avi` `.webm` `.flv` `.wmv` `.ts` `.m4v` |

> Files already converted are automatically skipped on re-runs.

---

## 🎬 Batch Video Downloader

I save a lot of reference videos for editing inspiration — tutorials, transitions, effects, clips from different platforms. Copying links one by one into a downloader app is slow. This lets me paste a whole bunch of links from any site into a text file and download them all at once, at the quality I want.

### Requirements

```bash
pip install yt-dlp
```

- [FFmpeg](https://ffmpeg.org/download.html) — recommended for video+audio merging

### Folder Structure

```
📁 your-folder/
├── downloader.py
├── links.txt            ← paste your video links here
├── downloadedfiles.txt  ← auto-created, logs completed downloads
└── Output/              ← auto-created, all downloaded videos saved here
```

### Usage

**Step 1** — Add links to `links.txt`, one per line:

```
https://www.youtube.com/watch?v=...
https://www.tiktok.com/@user/video/...
https://www.instagram.com/reel/...
https://www.facebook.com/watch?v=...
```

**Step 2** — Run the script:

```bash
python downloader.py
```

**Step 3** — It scans all links and shows the best quality available for each before you choose:

```
  🔍  Scanning available quality...

  [1/3] YouTube      ▸ Best available: 1080p      https://youtube.com/...
  [2/3] TikTok       ▸ Best available: 720p       https://tiktok.com/...
  [3/3] Instagram    ▸ Best available: 480p       https://instagram.com/...
```

**Step 4** — Pick your quality:

```
  [1]  2160p (4K)  — falls back to best available
  [2]  1080p (FHD) — falls back to best available
  [3]  720p  (HD)  — falls back to best available
  [4]  480p        — falls back to best available
  [5]  360p        — falls back to best available
  [6]  Best quality — always highest available
  [7]  Audio only  — MP3 192 kbps
```

> If your chosen quality isn't available for a video, it automatically falls back to the next best option — no errors, no skips.

### Supported Sites

| Platform | Notes |
|----------|-------|
| YouTube | Full support including Shorts |
| TikTok | Public videos |
| Facebook | Public videos |
| Instagram | Public reels and posts |
| Twitter / X | Public videos |
| Vimeo | Full support |
| Reddit | Video posts |
| + 1000 more | Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) |

### Smart Link Tracking

- ✅ **Downloaded** → removed from `links.txt`, logged to `downloadedfiles.txt` with timestamp + platform
- ❌ **Failed** → stays in `links.txt` so you can re-run and retry
- ⏭️ **Already downloaded** → automatically skipped on re-runs

### Example `downloadedfiles.txt`

```
2026-02-21 14:32 | YouTube      | https://youtube.com/watch?v=...
2026-02-21 14:33 | TikTok       | https://tiktok.com/@user/video/...
2026-02-21 14:34 | Instagram    | https://instagram.com/reel/...
```

---

## 🗂️ Large File Finder

Video editing eats storage fast. Raw footage, project files, renders — before you know it your drive is full. Instead of guessing what to delete, this script scans any drive or folder and lists the biggest files so you can decide what's worth keeping.

### Requirements

No extra packages needed — uses only Python's standard library.

### Usage

Open `find_large_files.py` and set your target drive and preferences at the bottom:

```python
drive = "D:\\"       # Change to the drive or folder you want to scan
TOP_N = 60           # How many files to list
MIN_SIZE_MB = 100    # Ignore files smaller than this (in MB)
```

Then run:

```bash
python find_large_files.py
```

### Example Output

```
Scanning D:\ … (this can take several minutes)
Skipping permission denied folders and broken symlinks

Top 10 largest files ≥ 100 MB on D:\

Size           │ Path
────────────────────────────────────────────────────────────────────────────────
  24.3 GiB     │ D:\Projects\footage\RAW_4K_shoot.mov
  12.1 GiB     │ D:\Projects\renders\final_export_v3.mp4
   8.7 GiB     │ D:\Games\SomeGame\gamedata.pak
   4.2 GiB     │ D:\Backups\old_backup_2024.zip
   ...

Total size of shown files : 49.3 GiB
Date: 2026-02-21 14:45
```

### Notes

- Skips system folders like `Windows`, `WinSxS`, `$RECYCLE.BIN`, `AppData` by default to avoid clutter — you can edit the `folders_to_skip` set in the script if needed
- Gracefully skips files with permission errors or that disappear mid-scan
- No files are deleted — this is read-only, purely for visibility

---

## 🎮 Roblox Anti-AFK

Sometimes you need to step away from Roblox without getting kicked. This script simulates small random movement bursts every 4–6 minutes to keep your character active — enough to fool the AFK detection without being too obvious.

### Requirements

```bash
pip install pydirectinput keyboard
```

### Usage

1. Open Roblox and get into your game
2. Run the script:

```bash
python anti_afk.py
```

3. Click into the Roblox window to make sure it's focused
4. Press **ESC** anytime to stop cleanly

### How It Works

Every 4 to 6 minutes (randomized so it doesn't look like a bot), it presses a short random sequence of `W`, `A`, `S`, `D`, and `Space` with human-like timing and small delays between each key. The randomness in both timing and key choice makes it look natural.

```
Anti-AFK started. Press ESC anytime to stop.
Make sure Roblox window is active / focused.
Will press random movement + jump every 4–6 minutes.

Waiting 5 min 23 sec...
→ Did a short movement/jump burst
Waiting 4 min 47 sec...
→ Did a short movement/jump burst
```

> ⚠️ Use responsibly and only in games/servers where this is acceptable. Some games have strict rules against automation.

---

## 🛠️ Requirements Summary

| Tool | Python Packages | External |
|------|----------------|----------|
| PDF ↔ Word | `python-docx` `docx2pdf` `pdf2docx` | — |
| Audio / Video Converter | — | FFmpeg |
| Video Downloader | `yt-dlp` | FFmpeg (recommended) |
| Large File Finder | — | — |
| Roblox Anti-AFK | `pydirectinput` `keyboard` | — |

### Install all Python packages at once

```bash
pip install python-docx docx2pdf pdf2docx yt-dlp pydirectinput keyboard
```

### Install FFmpeg

- **Windows**: `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

---

## 📝 Notes

- **Python 3.8+** required
- All scripts are standalone — each one works on its own, no shared dependencies between them
- Primarily built and tested on **Windows**, but the converter and downloader scripts should work on macOS and Linux too
- For private Instagram/Facebook content, you may need to pass browser cookies to yt-dlp

---

## 📃 License

MIT — free to use, modify, and share. If it helped you, that's enough. ✌️