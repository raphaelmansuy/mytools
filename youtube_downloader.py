#!/usr/bin/env -S uv run

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "yt-dlp"
# ]
# ///

import sys
import yt_dlp

# This script downloads public YouTube videos using yt-dlp.
# For most videos, cookies are NOT required. If you encounter age or region restrictions, see yt-dlp docs.

def download_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [on_progress],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"Title: {info['title']}")
            print("Download completed successfully!")
    except Exception as e:
        print(f"Error: {e}")

def on_progress(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} at {d['_speed_str']}, ETA {d['_eta_str']}", end='\r')
    elif d['status'] == 'finished':
        print("Download finished")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./youtube_downloader.py <YouTube_URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    download_video(url)
