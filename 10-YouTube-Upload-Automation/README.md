# Module 10: YouTube Upload Automation

## Overview

This module covers how to automatically upload your generated videos to YouTube, including setting metadata, thumbnails, and scheduling uploads.

## YouTube API Setup

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name it (e.g., "YouTube Automation")
4. Click "Create"

### Step 2: Enable YouTube Data API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and click "Enable"

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: Your app name
   - User support email: Your email
   - Developer contact: Your email
   - Save and continue through all steps
4. Back to Credentials → "Create Credentials" → "OAuth client ID"
5. Application type: "Desktop app"
6. Name it and click "Create"
7. Download the JSON file
8. Rename it to `client_secrets.json`

### Step 4: Install Required Packages

```bash
pip install google-auth-oauthlib google-api-python-client
```

## YouTube Upload Script

```python
#!/usr/bin/env python3
"""
YouTube Video Uploader
Automatically uploads videos to YouTube with metadata

First-time setup:
1. Place client_secrets.json in the same directory
2. Run the script - it will open a browser for authentication
3. After authentication, a token.pickle file is created for future use
"""

import os
import pickle
import json
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

class YouTubeUploader:
    """Handles YouTube video uploads and management"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtube.force-ssl'
    ]
    
    # YouTube category IDs
    CATEGORIES = {
        'film': '1',
        'autos': '2',
        'music': '10',
        'pets': '15',
        'sports': '17',
        'travel': '19',
        'gaming': '20',
        'vlogging': '22',
        'comedy': '23',
        'entertainment': '24',
        'news': '25',
        'howto': '26',
        'education': '27',
        'science': '28',
        'nonprofit': '29'
    }
    
    def __init__(self, credentials_file='client_secrets.json', token_file='token.pickle'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.youtube = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API"""
        creds = None
        
        # Load existing credentials
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing access token...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "Please download OAuth credentials from Google Cloud Console"
                    )
                
                print("Opening browser for authentication...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=8080)
            
            # Save credentials
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
            print("Credentials saved for future use")
        
        return build('youtube', 'v3', credentials=creds)
    
    def upload_video(self, video_file, title, description, tags=None,
                    category='education', privacy='private',
                    thumbnail_file=None, playlist_id=None,
                    scheduled_time=None):
        """
        Upload a video to YouTube
        
        Parameters:
        - video_file: Path to video file
        - title: Video title (max 100 chars)
        - description: Video description (max 5000 chars)
        - tags: List of tags
        - category: Category name or ID
        - privacy: 'private', 'unlisted', or 'public'
        - thumbnail_file: Path to thumbnail image
        - playlist_id: Add to playlist after upload
        - scheduled_time: datetime for scheduled publish (requires privacy='private')
        
        Returns:
        - Video ID if successful
        """
        print(f"\nUploading: {title}")
        print(f"File: {video_file}")
        
        # Validate file exists
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Video file not found: {video_file}")
        
        # Get category ID
        category_id = self.CATEGORIES.get(category.lower(), category)
        
        # Build request body
        body = {
            'snippet': {
                'title': title[:100],  # Max 100 chars
                'description': description[:5000],  # Max 5000 chars
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Add scheduled publish time if specified
        if scheduled_time and privacy == 'private':
            body['status']['publishAt'] = scheduled_time.isoformat() + 'Z'
            body['status']['privacyStatus'] = 'private'
        
        # Create media upload
        media = MediaFileUpload(
            video_file,
            mimetype='video/mp4',
            resumable=True,
            chunksize=1024*1024  # 1MB chunks
        )
        
        try:
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            print("Uploading", end="")
            
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(".", end="", flush=True)
            
            video_id = response['id']
            print(f"\nUpload complete!")
            print(f"Video ID: {video_id}")
            print(f"URL: https://youtube.com/watch?v={video_id}")
            
            # Set thumbnail if provided
            if thumbnail_file:
                self.set_thumbnail(video_id, thumbnail_file)
            
            # Add to playlist if specified
            if playlist_id:
                self.add_to_playlist(video_id, playlist_id)
            
            return video_id
            
        except HttpError as e:
            print(f"\nUpload failed: {e}")
            raise
    
    def set_thumbnail(self, video_id, thumbnail_file):
        """Set custom thumbnail for a video"""
        print(f"Setting thumbnail: {thumbnail_file}")
        
        if not os.path.exists(thumbnail_file):
            print(f"Warning: Thumbnail file not found: {thumbnail_file}")
            return False
        
        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_file)
            ).execute()
            print("Thumbnail set successfully")
            return True
        except HttpError as e:
            print(f"Failed to set thumbnail: {e}")
            return False
    
    def add_to_playlist(self, video_id, playlist_id):
        """Add video to a playlist"""
        print(f"Adding to playlist: {playlist_id}")
        
        try:
            self.youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()
            print("Added to playlist successfully")
            return True
        except HttpError as e:
            print(f"Failed to add to playlist: {e}")
            return False
    
    def create_playlist(self, title, description='', privacy='public'):
        """Create a new playlist"""
        print(f"Creating playlist: {title}")
        
        try:
            response = self.youtube.playlists().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': title,
                        'description': description
                    },
                    'status': {
                        'privacyStatus': privacy
                    }
                }
            ).execute()
            
            playlist_id = response['id']
            print(f"Playlist created: {playlist_id}")
            return playlist_id
        except HttpError as e:
            print(f"Failed to create playlist: {e}")
            return None
    
    def get_channel_info(self):
        """Get information about the authenticated channel"""
        response = self.youtube.channels().list(
            part='snippet,statistics',
            mine=True
        ).execute()
        
        if response['items']:
            channel = response['items'][0]
            return {
                'id': channel['id'],
                'title': channel['snippet']['title'],
                'subscribers': channel['statistics'].get('subscriberCount', 'Hidden'),
                'views': channel['statistics']['viewCount'],
                'videos': channel['statistics']['videoCount']
            }
        return None
    
    def list_my_videos(self, max_results=10):
        """List videos on the authenticated channel"""
        response = self.youtube.search().list(
            part='snippet',
            forMine=True,
            type='video',
            maxResults=max_results
        ).execute()
        
        videos = []
        for item in response.get('items', []):
            videos.append({
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'published': item['snippet']['publishedAt']
            })
        
        return videos


# ==================== BATCH UPLOAD ====================

def batch_upload(uploader, videos_config):
    """
    Upload multiple videos
    
    videos_config: List of dicts with:
        - video_file: Path to video
        - title: Video title
        - description: Video description
        - tags: List of tags
        - thumbnail: Path to thumbnail (optional)
    """
    results = []
    
    for i, config in enumerate(videos_config):
        print(f"\n{'='*50}")
        print(f"Uploading video {i+1}/{len(videos_config)}")
        print(f"{'='*50}")
        
        try:
            video_id = uploader.upload_video(
                video_file=config['video_file'],
                title=config['title'],
                description=config['description'],
                tags=config.get('tags', []),
                thumbnail_file=config.get('thumbnail'),
                privacy=config.get('privacy', 'private')
            )
            
            results.append({
                'title': config['title'],
                'video_id': video_id,
                'status': 'success'
            })
            
        except Exception as e:
            results.append({
                'title': config['title'],
                'error': str(e),
                'status': 'failed'
            })
    
    return results


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Initialize uploader
    uploader = YouTubeUploader()
    
    # Get channel info
    channel = uploader.get_channel_info()
    if channel:
        print(f"\nChannel: {channel['title']}")
        print(f"Subscribers: {channel['subscribers']}")
        print(f"Total views: {channel['views']}")
    
    # Upload a single video
    video_id = uploader.upload_video(
        video_file="output/final_video.mp4",
        title="5 AI Tools That Will Change Your Life",
        description="""In this video, we explore 5 amazing AI tools that will transform your productivity.

📌 TIMESTAMPS:
0:00 - Introduction
1:00 - Tool #1: ChatGPT
3:00 - Tool #2: Notion AI
5:00 - Tool #3: Grammarly
7:00 - Tool #4: Otter.ai
9:00 - Tool #5: Canva AI
11:00 - Conclusion

🔔 SUBSCRIBE for more AI content!

#AI #productivity #tools""",
        tags=["AI", "productivity", "tools", "artificial intelligence", "tutorial"],
        category="education",
        privacy="private",  # Start private, review, then make public
        thumbnail_file="thumbnails/thumbnail.png"
    )
    
    print(f"\nVideo uploaded successfully!")
    print(f"Review at: https://studio.youtube.com/video/{video_id}/edit")
```

## Scheduled Upload Script

```python
#!/usr/bin/env python3
"""
Scheduled YouTube Uploader
Schedule videos to be published at specific times
"""

from youtube_uploader import YouTubeUploader
from datetime import datetime, timedelta
import json
import os

class ScheduledUploader:
    def __init__(self):
        self.uploader = YouTubeUploader()
        self.schedule_file = 'upload_schedule.json'
    
    def schedule_video(self, video_file, title, description, tags,
                      publish_date, publish_time="09:00",
                      thumbnail=None):
        """
        Schedule a video for future publication
        
        publish_date: "YYYY-MM-DD" format
        publish_time: "HH:MM" format (24-hour)
        """
        # Parse scheduled time
        scheduled_datetime = datetime.strptime(
            f"{publish_date} {publish_time}",
            "%Y-%m-%d %H:%M"
        )
        
        # Upload as private with scheduled publish time
        video_id = self.uploader.upload_video(
            video_file=video_file,
            title=title,
            description=description,
            tags=tags,
            privacy='private',
            thumbnail_file=thumbnail,
            scheduled_time=scheduled_datetime
        )
        
        # Save to schedule
        self._save_to_schedule({
            'video_id': video_id,
            'title': title,
            'scheduled_time': scheduled_datetime.isoformat(),
            'status': 'scheduled'
        })
        
        print(f"\nVideo scheduled for: {scheduled_datetime}")
        return video_id
    
    def schedule_weekly_uploads(self, videos, start_date, days_between=3):
        """
        Schedule multiple videos with regular intervals
        
        videos: List of video configs
        start_date: "YYYY-MM-DD" first publish date
        days_between: Days between each video
        """
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        for video in videos:
            self.schedule_video(
                video_file=video['video_file'],
                title=video['title'],
                description=video['description'],
                tags=video.get('tags', []),
                publish_date=current_date.strftime("%Y-%m-%d"),
                publish_time=video.get('publish_time', "09:00"),
                thumbnail=video.get('thumbnail')
            )
            
            current_date += timedelta(days=days_between)
    
    def _save_to_schedule(self, video_info):
        """Save video to schedule file"""
        schedule = []
        
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r') as f:
                schedule = json.load(f)
        
        schedule.append(video_info)
        
        with open(self.schedule_file, 'w') as f:
            json.dump(schedule, f, indent=2)
    
    def view_schedule(self):
        """View all scheduled videos"""
        if not os.path.exists(self.schedule_file):
            print("No videos scheduled")
            return []
        
        with open(self.schedule_file, 'r') as f:
            schedule = json.load(f)
        
        print("\nScheduled Videos:")
        print("-" * 50)
        for video in schedule:
            print(f"  {video['scheduled_time']}: {video['title']}")
            print(f"    ID: {video['video_id']}")
        
        return schedule


if __name__ == "__main__":
    scheduler = ScheduledUploader()
    
    # Schedule a single video
    scheduler.schedule_video(
        video_file="output/video1.mp4",
        title="AI Productivity Tips",
        description="Learn how to use AI for productivity...",
        tags=["AI", "productivity"],
        publish_date="2024-12-20",
        publish_time="09:00",
        thumbnail="thumbnails/thumb1.png"
    )
    
    # Or schedule multiple videos
    videos = [
        {
            'video_file': 'output/video1.mp4',
            'title': 'Video 1 Title',
            'description': 'Description...',
            'tags': ['tag1', 'tag2'],
            'thumbnail': 'thumbnails/thumb1.png'
        },
        {
            'video_file': 'output/video2.mp4',
            'title': 'Video 2 Title',
            'description': 'Description...',
            'tags': ['tag1', 'tag2'],
            'thumbnail': 'thumbnails/thumb2.png'
        }
    ]
    
    scheduler.schedule_weekly_uploads(
        videos=videos,
        start_date="2024-12-20",
        days_between=3  # Monday and Thursday
    )
    
    # View schedule
    scheduler.view_schedule()
```

## Complete Upload Workflow

```python
#!/usr/bin/env python3
"""
Complete Upload Workflow
From generated video to published on YouTube
"""

import os
import json
from youtube_uploader import YouTubeUploader

def upload_from_project(project_dir, privacy='private'):
    """
    Upload video from automation pipeline project
    
    Expects project structure:
    project_dir/
    ├── output/final_video.mp4
    ├── thumbnails/thumbnail.png
    └── metadata/metadata.json
    """
    # Load metadata
    metadata_path = os.path.join(project_dir, 'metadata', 'metadata.json')
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Get file paths
    video_file = os.path.join(project_dir, 'output', 'final_video.mp4')
    thumbnail_file = os.path.join(project_dir, 'thumbnails', 'thumbnail.png')
    
    # Initialize uploader
    uploader = YouTubeUploader()
    
    # Upload video
    video_id = uploader.upload_video(
        video_file=video_file,
        title=metadata['titles'][0],  # Use first title option
        description=metadata['description'],
        tags=metadata['tags'],
        category='education',
        privacy=privacy,
        thumbnail_file=thumbnail_file if os.path.exists(thumbnail_file) else None
    )
    
    # Save upload info
    upload_info = {
        'video_id': video_id,
        'url': f'https://youtube.com/watch?v={video_id}',
        'studio_url': f'https://studio.youtube.com/video/{video_id}/edit',
        'uploaded_at': datetime.now().isoformat()
    }
    
    upload_info_path = os.path.join(project_dir, 'metadata', 'upload_info.json')
    with open(upload_info_path, 'w') as f:
        json.dump(upload_info, f, indent=2)
    
    print(f"\nUpload complete!")
    print(f"Video URL: {upload_info['url']}")
    print(f"Edit in Studio: {upload_info['studio_url']}")
    
    return upload_info


if __name__ == "__main__":
    from datetime import datetime
    
    # Upload from project directory
    upload_info = upload_from_project(
        project_dir="projects/my_first_video",
        privacy="private"  # Review before making public
    )
```

## API Quota Management

YouTube API has daily quotas. Here's how to manage them:

| Operation | Quota Cost |
|-----------|------------|
| Upload video | 1600 units |
| Set thumbnail | 50 units |
| Add to playlist | 50 units |
| Search | 100 units |
| List videos | 1 unit |

**Daily limit**: 10,000 units (free tier)
**Practical limit**: ~6 video uploads per day

### Quota-Aware Uploader

```python
#!/usr/bin/env python3
"""
Quota-Aware YouTube Uploader
Tracks API usage to avoid hitting limits
"""

import os
import json
from datetime import datetime, date

class QuotaTracker:
    def __init__(self, quota_file='quota_usage.json', daily_limit=10000):
        self.quota_file = quota_file
        self.daily_limit = daily_limit
        self.usage = self._load_usage()
    
    def _load_usage(self):
        """Load usage from file"""
        if os.path.exists(self.quota_file):
            with open(self.quota_file, 'r') as f:
                data = json.load(f)
                # Reset if new day
                if data.get('date') != str(date.today()):
                    return {'date': str(date.today()), 'used': 0}
                return data
        return {'date': str(date.today()), 'used': 0}
    
    def _save_usage(self):
        """Save usage to file"""
        with open(self.quota_file, 'w') as f:
            json.dump(self.usage, f)
    
    def can_upload(self, num_videos=1):
        """Check if we have quota for uploads"""
        cost = num_videos * 1700  # Upload + thumbnail
        return (self.usage['used'] + cost) <= self.daily_limit
    
    def record_upload(self):
        """Record an upload"""
        self.usage['used'] += 1700
        self._save_usage()
    
    def get_remaining_uploads(self):
        """Get number of uploads remaining today"""
        remaining_quota = self.daily_limit - self.usage['used']
        return remaining_quota // 1700
    
    def get_status(self):
        """Get quota status"""
        return {
            'date': self.usage['date'],
            'used': self.usage['used'],
            'remaining': self.daily_limit - self.usage['used'],
            'uploads_remaining': self.get_remaining_uploads()
        }


# Usage
tracker = QuotaTracker()
status = tracker.get_status()
print(f"Quota remaining: {status['remaining']}")
print(f"Uploads remaining today: {status['uploads_remaining']}")
```

## Upload Checklist

Before uploading:

- [ ] Video file exists and plays correctly
- [ ] Thumbnail is 1280x720 or larger
- [ ] Title is under 100 characters
- [ ] Description is under 5000 characters
- [ ] Tags are relevant and under 500 characters total
- [ ] client_secrets.json is in place
- [ ] Sufficient API quota available

After uploading:

- [ ] Video appears in YouTube Studio
- [ ] Thumbnail is set correctly
- [ ] Review video for any issues
- [ ] Add end screens and cards
- [ ] Set publish time or make public

## Next Steps

1. Set up YouTube API credentials
2. Test with a private upload
3. Create your upload workflow
4. Move to Module 11 for analytics

---

## Additional Resources

- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [YouTube Studio](https://studio.youtube.com/)
- [API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
