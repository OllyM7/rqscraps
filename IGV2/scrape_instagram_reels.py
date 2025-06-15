#!/usr/bin/env python3
"""
Instagram Reels Analytics Scraper

This script fetches analytics data for Instagram Reels from a public account,
including follower count, view counts, like counts, and media URLs.
"""

import os
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import instaloader
from tqdm import tqdm
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

class InstagramReelsScraper:
    def __init__(self, download_thumbnails: bool = False):
        """
        Initialize the Instagram Reels Scraper.
        
        Args:
            download_thumbnails (bool): Whether to download thumbnails to a local folder
        """
        self.L = instaloader.Instaloader(
            download_videos=False,
            download_video_thumbnails=download_thumbnails,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )
        
        # Try to load session if available
        try:
            self.L.load_session_from_file('sup3raw3somedud3')
        except:
            print("⚠️  No session file found. Some data might be limited.")

    def get_profile_data(self, username: str) -> Dict:
        """
        Fetch profile data and reels for a given username.
        
        Args:
            username (str): Instagram username to scrape
            
        Returns:
            Dict: Profile data including follower count and reels
        """
        try:
            profile = instaloader.Profile.from_username(self.L.context, username)
            
            # Get follower count
            follower_count = profile.followers
            
            # Get reels
            reels = []
            reel_count = 0
            
            print(f"📊 Fetching reels for @{username}...")
            for post in tqdm(profile.get_posts(), desc="Processing posts"):
                try:
                    if post.is_video and post.typename == "GraphVideo":
                        reel_data = {}
                        shortcode = getattr(post, 'shortcode', None)
                        if shortcode:
                            reel_data["reel_url"] = f"https://www.instagram.com/reel/{shortcode}/"
                        view_count = getattr(post, 'video_view_count', None)
                        if view_count is not None:
                            reel_data["view_count"] = view_count
                        like_count = getattr(post, 'likes', None)
                        if like_count is not None:
                            reel_data["like_count"] = like_count
                        thumbnail_url = getattr(post, 'url', None)
                        if thumbnail_url:
                            reel_data["thumbnail_url"] = thumbnail_url
                        caption = getattr(post, 'caption', None)
                        if caption:
                            reel_data["caption"] = caption
                        timestamp = getattr(post, 'date_local', None)
                        if timestamp:
                            reel_data["timestamp"] = timestamp.isoformat()
                        # Only add the reel if it has at least a URL
                        if "reel_url" in reel_data:
                            reels.append(reel_data)
                            reel_count += 1
                        if reel_count >= 12:
                            break
                except Exception as e:
                    print(f"⚠️  Skipping a post due to error: {e}")
            
            return {
                "username": username,
                "follower_count": follower_count,
                "reels_count": len(reels),
                "reels": reels,
                "scraped_at": datetime.now().isoformat()
            }
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"❌ Profile @{username} does not exist")
            return {"error": "Profile does not exist"}
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            print(f"❌ Profile @{username} is private")
            return {"error": "Private profile"}
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print(f"Exception args: {getattr(e, 'args', None)}")
            # Try to print response content if available
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print('Raw response:', e.response.text)
                except Exception as resp_e:
                    print('Could not print raw response:', resp_e)
            traceback.print_exc()
            return {"error": str(e)}

    def save_to_json(self, data: Dict, username: str) -> None:
        """Save the scraped data to a JSON file."""
        filename = f"{username}_reels_analytics.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Data saved to {filename}")

    def save_to_csv(self, data: Dict, username: str) -> None:
        """Save the scraped data to a CSV file."""
        import csv
        
        filename = f"{username}_reels_analytics.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['Username', 'Follower Count', 'Reel URL', 'View Count', 
                           'Like Count', 'Thumbnail URL', 'Caption', 'Timestamp'])
            
            # Write data
            for reel in data.get('reels', []):
                writer.writerow([
                    data['username'],
                    data['follower_count'],
                    reel['reel_url'],
                    reel['view_count'],
                    reel['like_count'],
                    reel['thumbnail_url'],
                    reel['caption'],
                    reel['timestamp']
                ])
        print(f"✅ Data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Scrape Instagram Reels Analytics')
    parser.add_argument('username', help='Instagram username to scrape')
    parser.add_argument('--download-thumbnails', action='store_true', 
                       help='Download thumbnails to local folder')
    parser.add_argument('--format', choices=['json', 'csv', 'both'], default='json',
                       help='Output format (default: json)')
    
    args = parser.parse_args()
    
    scraper = InstagramReelsScraper(download_thumbnails=args.download_thumbnails)
    data = scraper.get_profile_data(args.username)
    
    if 'error' not in data:
        if args.format in ['json', 'both']:
            scraper.save_to_json(data, args.username)
        if args.format in ['csv', 'both']:
            scraper.save_to_csv(data, args.username)

if __name__ == "__main__":
    main() 