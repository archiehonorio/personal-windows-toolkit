#!/usr/bin/env python3
"""
🎬 Batch Video Downloader
Supports: YouTube, TikTok, Facebook, Instagram (and 1000+ more sites via yt-dlp)

Setup:
    pip install yt-dlp

How to use:
    1. Paste your video links into links.txt  (one link per line)
    2. Run:  python downloader.py
    3. Choose quality
    4. Done! Videos saved to Output/
    5. Downloaded links are moved to downloadedfiles.txt automatically
"""

import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime

# Use the same Python that's running this script to call yt-dlp
YT_DLP = [sys.executable, "-m", "yt_dlp"]

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR      = Path(__file__).parent.resolve()
LINKS_FILE      = SCRIPT_DIR / "links.txt"
DOWNLOADED_FILE = SCRIPT_DIR / "downloadedfiles.txt"
OUTPUT_FOLDER   = SCRIPT_DIR / "Output"

# ── Quality presets ───────────────────────────────────────────────────────────
QUALITY_PRESETS = {
    "1": {
        "label": "2160p (4K)  — falls back to best available",
        "format": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]/best",
    },
    "2": {
        "label": "1080p (FHD) — falls back to best available",
        "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
    },
    "3": {
        "label": "720p  (HD)  — falls back to best available",
        "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best",
    },
    "4": {
        "label": "480p        — falls back to best available",
        "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]/best",
    },
    "5": {
        "label": "360p        — falls back to best available",
        "format": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]/best",
    },
    "6": {
        "label": "Best quality — always highest available",
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
    },
    "7": {
        "label": "Audio only  — MP3 192 kbps",
        "format": "bestaudio/best",
        "audio_only": True,
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def check_yt_dlp():
    try:
        result = subprocess.run(
            YT_DLP + ["--version"],
            check=True, capture_output=True, text=True
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("\n❌  yt-dlp not found! Install it with:")
        print(f"    {sys.executable} -m pip install yt-dlp\n")
        sys.exit(1)


def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        print("⚠️   FFmpeg not found — video+audio merging may not work.")
        print("    Install from https://ffmpeg.org for best results.\n")
        return False


def detect_site(url: str) -> str:
    u = url.lower()
    if "youtube.com" in u or "youtu.be" in u:  return "YouTube"
    if "tiktok.com" in u:                       return "TikTok"
    if "facebook.com" in u or "fb.watch" in u:  return "Facebook"
    if "instagram.com" in u:                    return "Instagram"
    if "twitter.com" in u or "x.com" in u:      return "Twitter/X"
    if "vimeo.com" in u:                        return "Vimeo"
    if "reddit.com" in u:                       return "Reddit"
    return "Other"


def load_links() -> list:
    if not LINKS_FILE.exists():
        LINKS_FILE.write_text("# Paste your video links here, one per line\n", encoding="utf-8")
        print(f"\n  📄  Created links.txt — paste your links there and run again.\n")
        sys.exit(0)
    lines = LINKS_FILE.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]


def load_downloaded() -> set:
    if not DOWNLOADED_FILE.exists():
        return set()
    urls = set()
    for line in DOWNLOADED_FILE.read_text(encoding="utf-8").splitlines():
        match = re.search(r"https?://\S+", line)
        if match:
            urls.add(match.group())
    return urls


def mark_downloaded(url: str, site: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(DOWNLOADED_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {site:<12} | {url}\n")


def remove_from_links(url: str):
    if not LINKS_FILE.exists():
        return
    lines = LINKS_FILE.read_text(encoding="utf-8").splitlines()
    new_lines = [l for l in lines if url not in l]
    LINKS_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def get_best_quality(url: str) -> str:
    """Query yt-dlp for available formats and return the highest resolution string."""
    cmd = YT_DLP + ["--list-formats", "--no-playlist", "--quiet", url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        heights = [int(h) for h in re.findall(r"\b(2160|1440|1080|720|480|360|240|144)\b", output)]
        if heights:
            return f"{max(heights)}p"
        return "unknown"
    except Exception:
        return "unknown"


def download_video(url: str, fmt: str, audio_only: bool = False) -> bool:
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    output_template = str(OUTPUT_FOLDER / "%(uploader)s - %(title)s.%(ext)s")

    if audio_only:
        cmd = YT_DLP + [
            "--format", fmt,
            "--output", output_template,
            "--no-playlist",
            "--no-warnings",
            "--quiet",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "192K",
            "--print", "after_move:  ✅  Audio MP3 | %(title)s",
        ]
    else:
        cmd = YT_DLP + [
            "--format", fmt,
            "--output", output_template,
            "--merge-output-format", "mp4",
            "--no-playlist",
            "--no-warnings",
            "--quiet",                                               # silence all [download]/[Merger] noise
            "--print", "after_move:  ✅  %(height)sp | %(title)s",  # one clean line when done
        ]

    if any(s in url for s in ["instagram.com", "facebook.com", "fb.watch"]):
        cmd += ["--add-header", "User-Agent:Mozilla/5.0"]

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False


def display_quality_menu():
    print("\n" + "─" * 55)
    print("  Choose download quality:\n")
    for key, preset in QUALITY_PRESETS.items():
        print(f"  [{key}]  {preset['label']}")
    print("─" * 55)
    print("  ℹ️   If chosen quality isn't available, automatically")
    print("       picks the next best option.\n")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("      🎬  Batch Video Downloader")
    print("=" * 55)
    print("  Supports: YouTube · TikTok · Facebook")
    print("            Instagram · Twitter/X · Vimeo · Reddit")
    print("            and 1000+ more sites")
    print("=" * 55)

    version = check_yt_dlp()
    print(f"\n  ✅  yt-dlp {version} ready")
    check_ffmpeg()

    links = load_links()
    if not links:
        print(f"\n  📭  links.txt is empty — paste some video URLs and run again.\n")
        sys.exit(0)

    downloaded = load_downloaded()
    pending    = [l for l in links if l not in downloaded]
    skipped    = len(links) - len(pending)

    print(f"\n  📋  {len(links)} link(s) found in links.txt")
    if skipped:
        print(f"  ⏭️   {skipped} already downloaded (skipping)")
    print(f"  🔗  {len(pending)} to download")

    if not pending:
        print("\n  All links already downloaded! Add new ones to links.txt.\n")
        sys.exit(0)

    # ── Scan best available quality per link ──────────────────────────────────
    print(f"\n  🔍  Scanning available quality...\n")
    link_info = []
    for i, url in enumerate(pending, 1):
        site = detect_site(url)
        sys.stdout.write(f"  [{i}/{len(pending)}] {site:<12} — checking...  \r")
        sys.stdout.flush()
        best = get_best_quality(url)
        short_url = url if len(url) <= 50 else url[:47] + "..."
        print(f"  [{i}/{len(pending)}] {site:<12} ▸ Best available: {best:<10} {short_url}")
        link_info.append((url, site, best))

    # ── Quality selection ─────────────────────────────────────────────────────
    display_quality_menu()
    while True:
        choice = input("  Enter quality number: ").strip()
        if choice in QUALITY_PRESETS:
            break
        print("  ⚠️   Invalid choice. Enter a number from the menu.")

    preset     = QUALITY_PRESETS[choice]
    audio_only = preset.get("audio_only", False)
    print(f"\n  Selected: {preset['label']}")
    print(f"  Output  : Output/\n")
    print("=" * 55)

    # ── Download loop ─────────────────────────────────────────────────────────
    success_urls, failed_urls = [], []

    for i, (url, site, best) in enumerate(link_info, 1):
        print(f"\n  [{i}/{len(pending)}] {site} — downloading...")
        ok = download_video(url, preset["format"], audio_only)

        if ok:
            success_urls.append((url, site))
            mark_downloaded(url, site)
            remove_from_links(url)
        else:
            print(f"  ❌  Failed — kept in links.txt for retry")
            failed_urls.append(url)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print(f"  ✔  {len(success_urls)} downloaded successfully")
    print(f"  ✘  {len(failed_urls)} failed")
    if success_urls:
        print(f"  📂  Videos saved to: Output/")
        print(f"  📝  Logged in: downloadedfiles.txt")
    if failed_urls:
        print(f"  🔁  Failed links remain in links.txt — fix & retry")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()