#!/usr/bin/env python3
"""
PDF <-> Word Converter
Drop files into the 'FileConvert' folder, converted files go to 'OutputFile'.
Requires: pip install python-docx docx2pdf pdf2docx
"""

import os
import sys
from pathlib import Path


# ── Folder Setup ────────────────────────────────────────────────────────────
SCRIPT_DIR    = Path(__file__).parent.resolve()
INPUT_FOLDER  = SCRIPT_DIR / "FileConvert"
OUTPUT_FOLDER = SCRIPT_DIR / "OutputFile"

SUPPORTED = {".pdf", ".doc", ".docx"}


def setup_folders():
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)


def check_dependencies():
    missing = []
    try:
        import docx       # noqa
    except ImportError:
        missing.append("python-docx")
    try:
        import docx2pdf   # noqa
    except ImportError:
        missing.append("docx2pdf")
    try:
        import pdf2docx   # noqa
    except ImportError:
        missing.append("pdf2docx")

    if missing:
        print(f"\n❌  Missing packages. Run:")
        print(f"    pip install {' '.join(missing)}\n")
        sys.exit(1)


# ── Converters ───────────────────────────────────────────────────────────────
def convert_word_to_pdf(input_path: Path) -> Path:
    from docx2pdf import convert
    output_path = OUTPUT_FOLDER / input_path.with_suffix(".pdf").name
    print(f"   🔄  Word → PDF")
    convert(str(input_path), str(output_path))
    return output_path


def convert_pdf_to_word(input_path: Path) -> Path:
    from pdf2docx import Converter
    output_path = OUTPUT_FOLDER / input_path.with_suffix(".docx").name
    print(f"   🔄  PDF → Word")
    cv = Converter(str(input_path))
    cv.convert(str(output_path), start=0, end=None)
    cv.close()
    return output_path


def convert_file(input_path: Path):
    ext = input_path.suffix.lower()
    print(f"\n📄  {input_path.name}")

    if ext in (".doc", ".docx"):
        output_path = convert_word_to_pdf(input_path)
    elif ext == ".pdf":
        output_path = convert_pdf_to_word(input_path)
    else:
        print(f"   ⚠️  Skipped (unsupported format: {ext})")
        return

    print(f"   ✅  Saved → OutputFile/{output_path.name}")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    setup_folders()
    check_dependencies()

    print("=" * 52)
    print("       📁  PDF ↔ Word Batch Converter")
    print("=" * 52)
    print(f"  Input  folder : {INPUT_FOLDER}")
    print(f"  Output folder : {OUTPUT_FOLDER}")
    print("=" * 52)

    # Collect supported files
    files = [f for f in INPUT_FOLDER.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED]

    if not files:
        print(f"\n  📭  No files found in FileConvert/")
        print(f"      Drop your .pdf, .doc, or .docx files there and run again.\n")
        sys.exit(0)

    print(f"\n  Found {len(files)} file(s) to convert...\n")

    success, failed = 0, 0
    for f in sorted(files):
        try:
            convert_file(f)
            success += 1
        except Exception as e:
            print(f"   ❌  Failed: {e}")
            failed += 1

    print("\n" + "=" * 52)
    print(f"  ✔  {success} converted   ✘  {failed} failed")
    print(f"  📂  Check your OutputFile folder!")
    print("=" * 52 + "\n")


if __name__ == "__main__":
    main()