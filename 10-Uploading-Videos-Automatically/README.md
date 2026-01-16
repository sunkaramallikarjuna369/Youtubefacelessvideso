# Module 10: Uploading Videos Automatically!

## Hey Krwutarth! Let's Upload Without Clicking!

You've made awesome videos - now let's get them on YouTube automatically! Instead of clicking through YouTube's upload page every time, we'll use code to do it for us!

## Important: Parent Help Needed!

For this module, you'll need your parent's help because:
1. YouTube API requires a Google Cloud account
2. You need to verify your identity
3. There are some technical setup steps

**Ask your parent to help you with the setup!**

## What is the YouTube API?

**API** = Application Programming Interface

It's a way for your code to talk to YouTube directly! Instead of clicking buttons on the website, your code sends commands to YouTube.

## Setting Up YouTube API (With Parent Help!)

### Step 1: Go to Google Cloud Console

1. Go to: https://console.cloud.google.com
2. Sign in with your Google account
3. Create a new project (call it "Krwutarth YouTube Uploader")

### Step 2: Enable YouTube Data API

1. In the search bar, type "YouTube Data API v3"
2. Click on it
3. Click "Enable"

### Step 3: Create Credentials

1. Go to "Credentials" in the left menu
2. Click "Create Credentials"
3. Choose "OAuth client ID"
4. Select "Desktop app"
5. Name it "Video Uploader"
6. Download the JSON file
7. Rename it to `client_secrets.json`
8. Put it in your youtube-videos folder

### Step 4: Install Required Libraries

Open Command Prompt and run:
```
pip install google-auth-oauthlib google-api-python-client
```

## Simple Video Uploader Script

Once you have the setup done, here's the script to upload videos:

```python
"""
Krwutarth's YouTube Uploader!
Upload videos to YouTube automatically!

SETUP REQUIRED:
1. Get client_secrets.json from Google Cloud Console
2. Put it in the same folder as this script
3. Run the script - it will open a browser for you to log in
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API settings
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Connect to YouTube with your account"""
    
    credentials = None
    
    # Check if we have saved credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # This will open a browser for you to log in
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES
            )
            credentials = flow.run_local_server(port=0)
        
        # Save credentials for next time
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    
    return build('youtube', 'v3', credentials=credentials)

def upload_video(video_file, title, description, tags, category="22"):
    """
    Upload a video to YouTube!
    
    video_file: Path to your video file
    title: Video title
    description: Video description
    tags: List of tags
    category: YouTube category (22 = People & Blogs)
    """
    
    print("=" * 50)
    print("KRWUTARTH'S YOUTUBE UPLOADER")
    print("=" * 50)
    print()
    
    # Connect to YouTube
    print("Connecting to YouTube...")
    youtube = get_authenticated_service()
    print("Connected!")
    print()
    
    # Video details
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category
        },
        'status': {
            'privacyStatus': 'private',  # Start as private for safety!
            'selfDeclaredMadeForKids': False
        }
    }
    
    # Upload the video
    print(f"Uploading: {video_file}")
    print("This may take a few minutes...")
    print()
    
    media = MediaFileUpload(
        video_file,
        chunksize=1024*1024,  # 1MB chunks
        resumable=True
    )
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"Upload progress: {progress}%")
    
    video_id = response['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    print()
    print("=" * 50)
    print("UPLOAD COMPLETE!")
    print("=" * 50)
    print(f"Video ID: {video_id}")
    print(f"Video URL: {video_url}")
    print()
    print("Note: Video is set to PRIVATE")
    print("Go to YouTube Studio to make it public when ready!")
    print("=" * 50)
    
    return video_id, video_url

# === MAIN PROGRAM ===
if __name__ == "__main__":
    
    # Your video details
    my_video = "my_first_youtube_video.mp4"  # Change this!
    my_title = "5 AMAZING Facts About Sharks!"
    my_description = """In this video, you'll discover 5 incredible facts about sharks!

If you enjoyed this video, please LIKE and SUBSCRIBE!
Turn on notifications so you never miss a video!

#sharks #facts #ocean #animals
"""
    my_tags = ["sharks", "shark facts", "ocean", "animals", "facts", "educational"]
    
    # Check if video exists
    if not os.path.exists(my_video):
        print(f"ERROR: Video file not found: {my_video}")
        print("Make sure the video file is in the same folder!")
    else:
        # Upload it!
        upload_video(my_video, my_title, my_description, my_tags)
    
    input("Press Enter to close...")
```

## Understanding Privacy Settings

When you upload, videos can be:

| Setting | Who Can See | Best For |
|---------|-------------|----------|
| Private | Only you | Testing, not ready yet |
| Unlisted | Anyone with link | Sharing with friends |
| Public | Everyone | When you're ready! |

**Always start with PRIVATE** until you're sure the video is good!

## Upload from Project Folder

Here's a script that uploads videos from your automated project folders:

```python
"""
Upload videos from project folders!
"""

import os
from youtube_uploader import upload_video

def upload_project(project_folder):
    """Upload a video from a project folder"""
    
    # Find the video file
    video_file = os.path.join(project_folder, "final_video.mp4")
    
    if not os.path.exists(video_file):
        print(f"No video found in: {project_folder}")
        return None
    
    # Read metadata
    metadata_file = os.path.join(project_folder, "metadata.txt")
    
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            content = f.read()
            
        # Parse metadata (simple parsing)
        lines = content.split("\n")
        title = ""
        description = ""
        tags = []
        
        current_section = None
        for line in lines:
            if line.startswith("TITLE:"):
                current_section = "title"
            elif line.startswith("DESCRIPTION:"):
                current_section = "description"
            elif line.startswith("TAGS:"):
                current_section = "tags"
            elif current_section == "title" and line.strip():
                title = line.strip()
            elif current_section == "description" and line.strip():
                description += line + "\n"
            elif current_section == "tags" and line.strip():
                tags = [t.strip() for t in line.split(",")]
    else:
        # Default metadata
        title = "My Awesome Video"
        description = "Check out this video!"
        tags = ["video", "awesome"]
    
    # Upload!
    return upload_video(video_file, title, description, tags)

# Upload a specific project
project = "project_20240115_sharks"  # Change to your project folder!
upload_project(project)
```

## Scheduling Uploads

Want to upload videos at specific times? YouTube lets you schedule when videos go public!

```python
"""
Schedule a video to go public at a specific time!
"""

from datetime import datetime, timedelta

def upload_scheduled(video_file, title, description, tags, publish_time):
    """
    Upload a video scheduled to go public later
    
    publish_time: When to make the video public (datetime object)
    """
    
    youtube = get_authenticated_service()
    
    # Format the time for YouTube
    publish_at = publish_time.isoformat() + "Z"
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': publish_at,  # Schedule time!
            'selfDeclaredMadeForKids': False
        }
    }
    
    # Upload...
    media = MediaFileUpload(video_file, resumable=True)
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = request.execute()
    
    print(f"Video scheduled to go public at: {publish_time}")
    return response

# Example: Schedule for tomorrow at 3 PM
tomorrow_3pm = datetime.now() + timedelta(days=1)
tomorrow_3pm = tomorrow_3pm.replace(hour=15, minute=0, second=0)

upload_scheduled(
    "my_video.mp4",
    "Amazing Video!",
    "Check this out!",
    ["awesome", "video"],
    tomorrow_3pm
)
```

## Adding Thumbnails

You can also upload custom thumbnails:

```python
"""
Set a custom thumbnail for your video!
"""

def set_thumbnail(video_id, thumbnail_file):
    """Upload a custom thumbnail for a video"""
    
    youtube = get_authenticated_service()
    
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_file)
    ).execute()
    
    print(f"Thumbnail set for video: {video_id}")

# Example
set_thumbnail("YOUR_VIDEO_ID", "thumbnail.jpg")
```

## YouTube API Limits

YouTube has daily limits on API usage:

| Action | Daily Limit |
|--------|-------------|
| Uploads | ~6 videos per day |
| API calls | 10,000 units |

**Don't worry!** For a beginner, these limits are plenty!

## Safety Tips

### 1. Always Start Private
Upload as private first, check the video, then make it public.

### 2. Keep Credentials Safe
Never share your `client_secrets.json` or `token.pickle` files!

### 3. Follow YouTube Rules
- No copyrighted content
- No inappropriate content
- Be honest in titles and descriptions

### 4. Ask Parents to Review
Before making videos public, have your parent check them!

## Your Assignment!

Before Module 11:

1. **Set up YouTube API** (with parent help!)
2. **Get your client_secrets.json file**
3. **Run the uploader script** with a test video
4. **Upload as PRIVATE first**
5. **Check it on YouTube Studio**

## Key Words to Remember

| Word | What It Means |
|------|---------------|
| API | Way for code to talk to websites |
| OAuth | Secure way to log in |
| Credentials | Your login information |
| Private | Only you can see |
| Public | Everyone can see |
| Scheduled | Set to go public at a specific time |

## Quick Quiz!

1. Why should you upload videos as private first?
2. What file do you need from Google Cloud Console?
3. What are the three privacy settings?
4. Why should you keep your credentials safe?

---

## Achievement Unlocked!

**"Upload Master"** - You can now upload videos automatically!

**Progress: Module 10 of 12 Complete!**

Next up: Module 11 - Tracking Your Success! Learn how to see your channel grow!
