#!/usr/bin/env -S uv run

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pytubefix"
# ]
# ///

import sys
from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_video(url, use_oauth=False, use_po_token=False):
    try:
        yt = YouTube(
            url,
            use_oauth=use_oauth,
            allow_oauth_cache=True,
            use_po_token=use_po_token,
            client="WEB",
            on_progress_callback=on_progress
        )
        
        print(f"Title: {yt.title}")
        ys = yt.streams.get_highest_resolution()
        ys.download()
        print("Download completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        if "private" in str(e).lower():
            print("Try running with OAuth authentication for private videos")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./downloader.py <YouTube_URL> [--oauth] [--po-token]")
        sys.exit(1)
    
    url = sys.argv[1]
    use_oauth = "--oauth" in sys.argv
    use_po_token = "--po-token" in sys.argv
    download_video(url, use_oauth, use_po_token)
