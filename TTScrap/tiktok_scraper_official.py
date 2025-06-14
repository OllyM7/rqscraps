from yt_dlp import YoutubeDL

def get_tiktok_video_metadata(url):
    ydl_opts = {
        "quiet": True,
        "force_generic_extractor": False,  # Let yt_dlp handle TikTok directly
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "username": info.get("uploader"),
                "description": info.get("description"),
                "views": info.get("view_count"),
                "likes": info.get("like_count"),
                "comments": info.get("comment_count"),
                "upload_date": info.get("upload_date"),
                "thumbnail": info.get("thumbnail"),
                "video_url": info.get("webpage_url"),
            }
    except Exception as e:
        print(f"❌ Failed to fetch video data: {e}")
        return None

# === Example usage ===
if __name__ == "__main__":
    video_url = "https://www.tiktok.com/@liloluvschomps/video/7515221269865073966"
    metadata = get_tiktok_video_metadata(video_url)

    if metadata:
        print("\n✅ TikTok Video Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
