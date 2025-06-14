
import sys
from yt_dlp import YoutubeDL

def extract_youtube_metadata(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "id": info.get("id"),
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "channel_id": info.get("channel_id"),
            "upload_date": info.get("upload_date"),
            "duration": info.get("duration"),
            "view_count": info.get("view_count"),
            "like_count": info.get("like_count"),
            "comment_count": info.get("comment_count"),
            "description": info.get("description"),
            "categories": info.get("categories"),
            "tags": info.get("tags"),
            "webpage_url": info.get("webpage_url"),
            "thumbnail": info.get("thumbnail"),
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please pass a YouTube video or shorts URL as an argument.")
        print("Example: python3 youtube_scraper.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        sys.exit(1)

    video_url = sys.argv[1]
    metadata = extract_youtube_metadata(video_url)

    import pprint
    pprint.pprint(metadata)