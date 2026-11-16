"""
VeriMath — Model Download Utility
==================================
Downloads the Phi-3 Mini GGUF (Q4_K_M quantized) model for local LLM inference.
Default target: ~/models or path specified in LLM_MODEL_PATH.
"""

import os
import sys
import urllib.request
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DEFAULT_URL = (
    "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/"
    "Phi-3-mini-4k-instruct-q4.gguf"
)

def download_file(url: str, dest_path: Path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists():
        print(f"File already exists at: {dest_path}")
        return

    print(f"Downloading model from:\n  {url}\nDestination:\n  {dest_path}")
    print("This file is ~2.2 GB. Download may take several minutes depending on internet speed...")

    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size) if total_size > 0 else 0
        mb_downloaded = (count * block_size) / (1024 * 1024)
        total_mb = total_size / (1024 * 1024) if total_size > 0 else 0
        sys.stdout.write(f"\rProgress: {percent}% [{mb_downloaded:.1f} MB / {total_mb:.1f} MB]")
        sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, str(dest_path), reporthook=reporthook)
        print("\nDownload complete! Model ready.")
    except Exception as e:
        print(f"\nFailed to download model: {e}")
        if dest_path.exists():
            dest_path.unlink()
        sys.exit(1)

def main():
    target_env = os.getenv("LLM_MODEL_PATH")
    if target_env:
        target_path = Path(target_env)
    else:
        target_path = Path(__file__).parent.parent / "models" / "phi-3-mini-4k-instruct-q4.gguf"

    download_file(DEFAULT_URL, target_path)

if __name__ == "__main__":
    main()
