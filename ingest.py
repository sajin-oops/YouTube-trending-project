import os
import json
from datetime import datetime
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def fetch_trending_videos(region_code="IN", max_results=50):
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video = {
            "video_id":        item["id"],
            "title":           item["snippet"]["title"],
            "channel_id":      item["snippet"]["channelId"],
            "channel_title":   item["snippet"]["channelTitle"],
            "category_id":     item["snippet"]["categoryId"],
            "published_at":    item["snippet"]["publishedAt"],
            "description":     item["snippet"]["description"][:500],
            "view_count":      int(item["statistics"].get("viewCount", 0)),
            "like_count":      int(item["statistics"].get("likeCount", 0)),
            "comment_count":   int(item["statistics"].get("commentCount", 0)),
            "duration":        item["contentDetails"]["duration"],
            "fetched_at": datetime.now(datetime.UTC).isoformat(),
            "region_code":     region_code
        }
        videos.append(video)

    print(f"✅ Fetched {len(videos)} trending videos for region: {region_code}")
    return videos


if __name__ == "__main__":
    videos = fetch_trending_videos(region_code="IN")
    # Save locally as JSON backup
    with open("raw_videos.json", "w") as f:
        json.dump(videos, f, indent=2)
    print("✅ Saved to raw_videos.json")