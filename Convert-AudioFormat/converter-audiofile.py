#!/usr/bin/env python3
"""
Audio / Video → Any Format Converter
Drop files into 'Input/', pick your output format, get results in 'Output/'.
Requires: FFmpeg installed and on PATH
"""

import subprocess
import sys
from pathlib import Path

# ── Folders ──────────────────────────────────────────────────────────────────
INPUT_FOLDER  = Path("Input")
OUTPUT_FOLDER = Path("Output")

# ── Supported input types ─────────────────────────────────────────────────────
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".aac", ".ogg", ".flac", ".wav", ".wma", ".opus", ".aiff"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv", ".ts", ".m4v"}
ALL_EXTENSIONS   = AUDIO_EXTENSIONS | VIDEO_EXTENSIONS

# ── Output format profiles ────────────────────────────────────────────────────
OUTPUT_FORMATS = {
    # Audio formats
    "1":  {"label": "WAV  — 22050 Hz mono 16-bit  (XTTS / TTS reference)",   "ext": ".wav",  "args": ["-ar", "22050", "-ac", "1", "-sample_fmt", "s16"]},
    "2":  {"label": "WAV  — 44100 Hz stereo 16-bit (standard CD quality)",    "ext": ".wav",  "args": ["-ar", "44100", "-ac", "2", "-sample_fmt", "s16"]},
    "3":  {"label": "MP3  — 192 kbps stereo",                                 "ext": ".mp3",  "args": ["-b:a", "192k", "-ac", "2"]},
    "4":  {"label": "MP3  — 320 kbps stereo (high quality)",                  "ext": ".mp3",  "args": ["-b:a", "320k", "-ac", "2"]},
    "5":  {"label": "AAC  — 192 kbps (iTunes / mobile friendly)",             "ext": ".m4a",  "args": ["-b:a", "192k", "-ac", "2"]},
    "6":  {"label": "FLAC — Lossless compressed audio",                       "ext": ".flac", "args": ["-compression_level", "8"]},
    "7":  {"label": "OGG  — Vorbis ~192 kbps",                                "ext": ".ogg",  "args": ["-q:a", "6"]},
    "8":  {"label": "OPUS — 128 kbps (best compression / quality ratio)",     "ext": ".opus", "args": ["-b:a", "128k"]},
    # Extract audio from video
    "9":  {"label": "MP3  — Extract audio from video (192 kbps)",             "ext": ".mp3",  "args": ["-vn", "-b:a", "192k"]},
    "10": {"label": "WAV  — Extract audio from video (44100 Hz stereo)",      "ext": ".wav",  "args": ["-vn", "-ar", "44100", "-ac", "2", "-sample_fmt", "s16"]},
    # Video formats
    "11": {"label": "MP4  — H.264 video, AAC audio (universal)",              "ext": ".mp4",  "args": ["-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "192k"]},
    "12": {"label": "MP4  — High quality H.264 (CRF 18)",                    "ext": ".mp4",  "args": ["-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k"]},
    "13": {"label": "MKV  — H.264 video, copy audio streams",                "ext": ".mkv",  "args": ["-c:v", "libx264", "-crf", "23", "-c:a", "copy"]},
    "14": {"label": "WEBM — VP9 video (web optimized)",                       "ext": ".webm", "args": ["-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0", "-c:a", "libopus"]},
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("\n❌  FFmpeg not found! Install it from https://ffmpeg.org and add it to your PATH.\n")
        sys.exit(1)


def scan_files():
    """Return all supported files found in INPUT_FOLDER."""
    files = []
    for f in INPUT_FOLDER.rglob("*"):
        if f.is_file() and f.suffix.lower() in ALL_EXTENSIONS:
            files.append(f)
    return sorted(files)


def display_files(files):
    print(f"\n  Found {len(files)} file(s) in Input/:\n")
    for i, f in enumerate(files, 1):
        kind = "🎵" if f.suffix.lower() in AUDIO_EXTENSIONS else "🎬"
        print(f"    {kind}  {f.relative_to(INPUT_FOLDER)}")


def display_format_menu():
    print("\n" + "─" * 58)
    print("  Choose output format:\n")
    print("  ── Audio ──────────────────────────────────────────────")
    for key in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        print(f"  [{key:>2}]  {OUTPUT_FORMATS[key]['label']}")
    print("\n  ── Extract Audio from Video ───────────────────────────")
    for key in ["9", "10"]:
        print(f"  [{key:>2}]  {OUTPUT_FORMATS[key]['label']}")
    print("\n  ── Video ──────────────────────────────────────────────")
    for key in ["11", "12", "13", "14"]:
        print(f"  [{key:>2}]  {OUTPUT_FORMATS[key]['label']}")
    print("─" * 58)


def convert_file(input_path: Path, output_path: Path, extra_args: list):
    if output_path.exists():
        print(f"  ⏭️   Skipped (already exists): {output_path.name}")
        return True

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        *extra_args,
        "-loglevel", "error",
        str(output_path)
    ]

    try:
        result = subprocess.run(cmd, check=True, stderr=subprocess.PIPE, text=True)
        print(f"  ✅  {input_path.name}  →  {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌  Failed: {input_path.name}")
        if e.stderr:
            print(f"      {e.stderr.strip()}")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    print("=" * 58)
    print("      🎧  Audio / Video Format Converter")
    print("=" * 58)
    print(f"  Input  → Input/")
    print(f"  Output → Output/")
    print("=" * 58)

    check_ffmpeg()

    if not INPUT_FOLDER.exists():
        print(f"\n  📭  'Input/' folder not found.")
        print(f"      Creating it now — drop your files there and run again.\n")
        INPUT_FOLDER.mkdir(parents=True)
        sys.exit(0)

    files = scan_files()
    if not files:
        print(f"\n  📭  No supported files found in Input/\n")
        sys.exit(0)

    display_files(files)
    display_format_menu()

    # Format selection
    while True:
        choice = input("\n  Enter format number: ").strip()
        if choice in OUTPUT_FORMATS:
            break
        print(f"  ⚠️   Invalid choice. Pick a number from the menu.")

    selected = OUTPUT_FORMATS[choice]
    print(f"\n  Selected: {selected['label']}")
    print(f"  Converting {len(files)} file(s)...\n")

    success, failed = 0, 0
    for file_path in files:
        relative    = file_path.relative_to(INPUT_FOLDER)
        output_name = relative.with_suffix(selected["ext"])
        output_path = OUTPUT_FOLDER / output_name

        ok = convert_file(file_path, output_path, selected["args"])
        if ok:
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 58)
    print(f"  ✔  {success} converted    ✘  {failed} failed")
    print(f"  📂  Results are in Output/")
    print("=" * 58 + "\n")


if __name__ == "__main__":
    main()