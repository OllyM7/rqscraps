# Instagram Reels Analytics Scraper

A Python tool that fetches analytics data for Instagram Reels from public accounts using the `instaloader` library.

## Features

- Fetches follower count for a given Instagram account
- Retrieves the last 12 reels with:
  - View count
  - Like count
  - Reel URL
  - Thumbnail URL
  - Caption
  - Timestamp
- Supports JSON and CSV output formats
- Optional thumbnail downloads
- Progress bar for tracking scraping progress
- Error handling for private accounts and non-existent profiles

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python scrape_instagram_reels.py username
```

### Options
- `--download-thumbnails`: Download thumbnails to local folder
- `--format`: Output format (json, csv, or both)
  ```bash
  python scrape_instagram_reels.py username --format both
  ```

### Examples

1. Basic usage (JSON output):
```bash
python scrape_instagram_reels.py nasa
```

2. Download thumbnails and save as CSV:
```bash
python scrape_instagram_reels.py nasa --download-thumbnails --format csv
```

3. Save in both formats:
```bash
python scrape_instagram_reels.py nasa --format both
```

## Output Format

### JSON Output
```json
{
  "username": "nasa",
  "follower_count": 96404868,
  "reels_count": 12,
  "reels": [
    {
      "reel_url": "https://www.instagram.com/reel/ABC123/",
      "view_count": 1000000,
      "like_count": 50000,
      "thumbnail_url": "https://...",
      "caption": "Post caption...",
      "timestamp": "2024-03-14T12:00:00"
    },
    // ... more reels
  ],
  "scraped_at": "2024-03-14T12:00:00"
}
```

### CSV Output
The CSV file will contain columns for:
- Username
- Follower Count
- Reel URL
- View Count
- Like Count
- Thumbnail URL
- Caption
- Timestamp

## Notes

- The script requires a public Instagram account
- Some data might be limited without an Instagram session
- Rate limiting may apply for frequent requests
- Thumbnails are downloaded to the current directory if requested

## License

MIT License 