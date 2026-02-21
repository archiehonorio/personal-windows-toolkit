# find_large_files.py
import os
from pathlib import Path
import heapq
from datetime import datetime

def sizeof_fmt(num, suffix="B"):
    """Convert bytes to human-readable format (like 12.4 GiB)"""
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def find_largest_files(root_dir, count=50, min_size_mb=50):
    """
    Returns the 'count' largest files under root_dir (at least min_size_mb)
    Skips permission errors, deleted files, symlinks, etc.
    """
    # Min size in bytes
    min_size = min_size_mb * 1024 * 1024

    # Max-heap (negative size so largest comes first)
    largest = []  # list of (-size, path)

    root = Path(root_dir).resolve()

    print(f"Scanning {root} … (this can take several minutes)")
    print("Skipping permission denied folders and broken symlinks\n")

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Optional: skip some very noisy/system folders (add more if you want)
        # You can comment out or modify this block
        folders_to_skip = {
            'Windows', 'WinSxS', 'System Volume Information',
            '$RECYCLE.BIN', 'ProgramData', 'AppData'
        }
        dirnames[:] = [d for d in dirnames if d not in folders_to_skip]

        for file in filenames:
            path = Path(dirpath) / file

            try:
                # Skip symlinks (avoid following broken or looping ones)
                if path.is_symlink():
                    continue

                size = path.stat().st_size

                if size < min_size:
                    continue

                # Keep only top N → heap of size N
                heapq.heappush(largest, (-size, str(path)))

                # If we have more than we need → drop smallest
                if len(largest) > count:
                    heapq.heappop(largest)

            except (FileNotFoundError, PermissionError, OSError):
                # File disappeared between listing & stat, or no permission → skip silently
                continue

    # Convert to list of (size, path) sorted descending
    result = [(-size, path) for size, path in largest]
    result.sort(reverse=True)  # largest first

    return result


if __name__ == "__main__":
    drive = "D:\\" # Change this to the target drive or folder path you want to search

    TOP_N = 60
    MIN_SIZE_MB = 100       # ignore anything smaller than 100 MB

    large_files = find_largest_files(drive, count=TOP_N, min_size_mb=MIN_SIZE_MB)

    if not large_files:
        print("No files ≥", MIN_SIZE_MB, "MB found (or access denied everywhere)")
    else:
        print(f"\nTop {len(large_files)} largest files ≥ {MIN_SIZE_MB} MB on {drive}\n")
        print("Size           │ Path")
        print("-" * 100)

        for size_bytes, path in large_files:
            print(f"{sizeof_fmt(size_bytes):>14}  │ {path}")

        total_size = sum(size for size, _ in large_files)
        print("\nTotal size of shown files : " + sizeof_fmt(total_size))
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")