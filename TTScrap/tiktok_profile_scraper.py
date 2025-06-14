import re
import requests
import subprocess
from yt_dlp import YoutubeDL
import sys
import os

def parse_count_string(s):
    s = s.replace(",", "").replace(" ", "")
    if "K" in s: return int(float(s.replace("K", "")) * 1_000)
    if "M" in s: return int(float(s.replace("M", "")) * 1_000_000)
    return int(s)

def get_tiktok_followers(username: str) -> int:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.tiktok.com/@{username}"
        html = requests.get(url, headers=headers).text
        match = re.search(r'"followerCount":\s?(\d+)', html)
        return int(match.group(1)) if match else 0
    except:
        return 0

def get_tiktok_avg_views(username: str, max_videos: int = 20) -> int:
    try:
        tiktok_url = f"https://www.tiktok.com/@{username}"
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "playlistend": max_videos,
            "no_warnings": True,
            "logger": DummyLogger(),
        }

        with YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(tiktok_url, download=False)
        entries = data.get("entries", [])[:max_videos]

        views = []
        for entry in entries:
            url = entry.get("url")
            full_url = url if url.startswith("http") else f"https://www.tiktok.com{url}"
            with YoutubeDL({"quiet": True, "no_warnings": True, "logger": DummyLogger()}) as ydl:
                info = ydl.extract_info(full_url, download=False)
                views.append(info.get("view_count", 0))
        return int(sum(views) / len(views)) if views else 0
    except:
        return 0

class DummyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

if __name__ == "__main__":
    username = input("Enter TikTok username: ").strip()
    followers = get_tiktok_followers(username)
    avg_views = get_tiktok_avg_views(username)

    result = {
        "username": username,
        "followers": followers,
        "average_views": avg_views
    }

    print("\n✅ TikTok Stats:")
    print(result)
