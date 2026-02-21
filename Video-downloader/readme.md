pip install yt-dlp
```
FFmpeg is also recommended for merging video+audio — grab it from ffmpeg.org if you don't have it.

**Every time:**
1. Paste your links into `links.txt` (one per line, any mix of sites)
2. Run `python downloader.py`
3. Pick quality and it downloads everything

**What the quality menu looks like:**
```
  [1]  2160p (4K)  — falls back to best available
  [2]  1080p (FHD) — falls back to best available
  [3]  720p  (HD)  — falls back to best available
  [4]  480p        — falls back to best available
  [5]  360p        — falls back to best available
  [6]  Best quality — always highest available
  [7]  Audio only  — MP3 192 kbps
```

Pick `1080p` and if a video only has 720p, it automatically downloads 720p — no errors, no skips.

**The smart link tracking:**
- ✅ Downloaded → removed from `links.txt`, logged to `downloadedfiles.txt` with timestamp + site name
- ❌ Failed → stays in `links.txt` so you can just run again to retry

Your folder structure will look like:
```
your-folder/
├── downloader.py
├── links.txt           ← paste links here
├── downloadedfiles.txt ← auto-created, logs done links
└── Output/             ← auto-created, all downloaded videos