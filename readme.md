# 🧰 Personal Windows Toolkit

A collection of lightweight Python scripts for everyday file and media tasks — no GUI needed, just drop files and run.

---

## 📦 What's Inside

| Tool | Description |
|------|-------------|
| [`converter.py`](#-pdf--word-converter) | Convert PDF ↔ Word automatically |
| [`converter_audio.py`](#-audio--video-format-converter) | Convert audio/video to any format via FFmpeg |
| [`downloader.py`](#-batch-video-downloader) | Download videos from YouTube, TikTok, Instagram, Facebook & more |

---

## 📄 PDF ↔ Word Converter

Automatically detects file type and converts in the right direction — no flags, no options.

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

Convert any audio or video file to your chosen format using FFmpeg. Supports extracting audio from video files too.

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

Download videos from YouTube, TikTok, Facebook, Instagram, and 1000+ other sites. Paste links into a text file and batch download with your chosen quality.

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

## 🛠️ Requirements Summary

| Tool | Python Packages | External |
|------|----------------|----------|
| PDF ↔ Word | `python-docx` `docx2pdf` `pdf2docx` | — |
| Audio / Video Converter | — | FFmpeg |
| Video Downloader | `yt-dlp` | FFmpeg (recommended) |

### Install all Python packages at once

```bash
pip install python-docx docx2pdf pdf2docx yt-dlp
```

### Install FFmpeg

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH, or use `winget install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

---

## 📝 Notes

- **Python 3.8+** required
- All scripts are standalone — run each independently
- Tested on Windows; should work on macOS and Linux too
- For private Instagram/Facebook content, you may need to pass cookies to yt-dlp

---

## 📃 License

MIT — free to use, modify, and distribute.