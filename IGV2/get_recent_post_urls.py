import instaloader
import sys

if len(sys.argv) < 2:
    print("Usage: python get_recent_post_urls.py <username> [count]")
    sys.exit(1)

username = sys.argv[1]
max_count = int(sys.argv[2]) if len(sys.argv) > 2 else 20

L = instaloader.Instaloader()
L.load_session_from_file('sup3raw3somedud3')

try:
    profile = instaloader.Profile.from_username(L.context, username)
    urls = []
    for post in profile.get_posts():
        # For reels, use /reel/; for regular posts, use /p/
        if post.typename == "GraphVideo" and post.is_video:
            urls.append(f"https://www.instagram.com/reel/{post.shortcode}/")
        else:
            urls.append(f"https://www.instagram.com/p/{post.shortcode}/")
        if len(urls) >= max_count:
            break
    print("\n".join(urls))
except Exception as e:
    print(f"❌ Error: {e}") 