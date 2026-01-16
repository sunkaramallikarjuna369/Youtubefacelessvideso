# Module 5: Finding Cool Videos & Pictures!

## Hey Krwutarth! Let's Get Free Visuals for Your Videos!

Your video needs more than just a voice - it needs cool pictures and video clips! The good news? You can get AMAZING visuals for FREE. Let me show you how!

## Why You Need Visuals

In a faceless video, visuals are EVERYTHING! While your voiceover talks, viewers need something interesting to look at.

**Example:** If you're talking about sharks, you show:
- Video clips of sharks swimming
- Pictures of different shark species
- Cool underwater footage

## Where to Get FREE Videos and Pictures

### 1. Pexels (BEST for Videos!)
**Website:** https://www.pexels.com

Pexels has THOUSANDS of free videos and photos. All free to use, even for making money!

**How to use it:**
1. Go to pexels.com
2. Type what you need (like "shark" or "space")
3. Click "Videos" to see video clips
4. Download what you like!

### 2. Pixabay (Great for Both!)
**Website:** https://pixabay.com

Another awesome free site with videos and images.

**How to use it:**
1. Go to pixabay.com
2. Search for what you need
3. Click "Videos" or "Photos"
4. Download for free!

### 3. Unsplash (Best for Photos!)
**Website:** https://unsplash.com

Beautiful high-quality photos, all free!

### 4. Coverr (Cool Video Clips!)
**Website:** https://coverr.co

Free video clips that look professional.

## Using the Pexels API (Automatic Downloads!)

Instead of downloading videos one by one, let's make a program that does it for you!

### Step 1: Get Your Pexels API Key

1. Go to: https://www.pexels.com/api/
2. Click "Get Started" or "Join"
3. Create a free account
4. After logging in, you'll see your API key
5. Copy it!

### Step 2: Create the Video Downloader

1. Open Notepad
2. Copy and paste this code:

```python
"""
Krwutarth's Video Finder!
Automatically download free videos from Pexels!
"""

import requests
import os

# PUT YOUR PEXELS API KEY HERE!
PEXELS_API_KEY = "YOUR_API_KEY_HERE"

def search_videos(query, num_videos=5):
    """Search for videos on Pexels"""
    
    print(f"Searching for videos about: {query}")
    print()
    
    # Pexels API URL
    url = "https://api.pexels.com/videos/search"
    
    # Set up the request
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    params = {
        "query": query,
        "per_page": num_videos,
        "orientation": "landscape"  # Wide videos for YouTube
    }
    
    # Make the request
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        videos = data.get("videos", [])
        print(f"Found {len(videos)} videos!")
        return videos
    else:
        print(f"Error: {response.status_code}")
        return []

def download_video(video, folder="downloads"):
    """Download a video to your computer"""
    
    # Create downloads folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Get the video file (medium quality is good for YouTube)
    video_files = video.get("video_files", [])
    
    # Find a good quality version
    best_file = None
    for vf in video_files:
        if vf.get("quality") == "hd" and vf.get("width", 0) >= 1280:
            best_file = vf
            break
    
    if not best_file and video_files:
        best_file = video_files[0]
    
    if not best_file:
        print("No video file found!")
        return None
    
    # Download the video
    video_url = best_file.get("link")
    video_id = video.get("id")
    filename = f"{folder}/video_{video_id}.mp4"
    
    print(f"Downloading video {video_id}...")
    
    response = requests.get(video_url, stream=True)
    
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Saved to: {filename}")
    return filename

# === MAIN PROGRAM ===
if __name__ == "__main__":
    print("=" * 50)
    print("KRWUTARTH'S VIDEO FINDER!")
    print("=" * 50)
    print()
    
    # What videos do you want?
    search_term = "ocean underwater"  # Change this!
    how_many = 3  # How many videos to download
    
    # Search for videos
    videos = search_videos(search_term, how_many)
    
    # Download each video
    if videos:
        print()
        print("Downloading videos...")
        print()
        
        for video in videos:
            download_video(video)
        
        print()
        print("All done! Check the 'downloads' folder!")
    else:
        print("No videos found. Try a different search term!")
    
    input("Press Enter to close...")
```

3. Save it as `video_finder.py`

### Step 3: Add Your API Key

Find this line in the code:
```python
PEXELS_API_KEY = "YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with your actual Pexels API key!

### Step 4: Run It!

1. Open Command Prompt in your youtube-videos folder
2. Type: `python video_finder.py`
3. Wait for downloads to finish
4. Check the "downloads" folder!

## Finding Pictures Too!

Here's a script to download pictures:

```python
"""
Krwutarth's Picture Finder!
Download free pictures from Pexels!
"""

import requests
import os

PEXELS_API_KEY = "YOUR_API_KEY_HERE"

def search_photos(query, num_photos=5):
    """Search for photos on Pexels"""
    
    print(f"Searching for photos: {query}")
    
    url = "https://api.pexels.com/v1/search"
    
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": num_photos,
        "orientation": "landscape"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        photos = data.get("photos", [])
        print(f"Found {len(photos)} photos!")
        return photos
    else:
        print(f"Error: {response.status_code}")
        return []

def download_photo(photo, folder="pictures"):
    """Download a photo"""
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Get large size photo
    photo_url = photo.get("src", {}).get("large2x")
    photo_id = photo.get("id")
    filename = f"{folder}/photo_{photo_id}.jpg"
    
    print(f"Downloading photo {photo_id}...")
    
    response = requests.get(photo_url)
    
    with open(filename, "wb") as f:
        f.write(response.content)
    
    print(f"Saved to: {filename}")
    return filename

# === MAIN PROGRAM ===
if __name__ == "__main__":
    print("=" * 50)
    print("KRWUTARTH'S PICTURE FINDER!")
    print("=" * 50)
    print()
    
    search_term = "dinosaur"  # Change this!
    how_many = 5
    
    photos = search_photos(search_term, how_many)
    
    if photos:
        print()
        for photo in photos:
            download_photo(photo)
        print()
        print("Done! Check the 'pictures' folder!")
    
    input("Press Enter to close...")
```

## Tips for Finding Great Visuals

### 1. Use Specific Search Terms
- Bad: "animal"
- Good: "shark swimming underwater"

### 2. Download More Than You Need
If you need 5 clips, download 10. Then pick the best ones!

### 3. Match Your Script
If your script says "The shark swims fast," find a video of a shark swimming fast!

### 4. Use Landscape Videos
YouTube videos are wide (landscape), so download landscape videos, not portrait!

### 5. Check Video Length
Short clips (5-15 seconds) work best. You'll combine many clips together.

## Organizing Your Downloads

Keep your files organized! Create folders like this:

```
youtube-videos/
├── project-sharks/
│   ├── videos/
│   │   ├── shark1.mp4
│   │   ├── shark2.mp4
│   │   └── shark3.mp4
│   ├── pictures/
│   │   ├── shark_photo1.jpg
│   │   └── shark_photo2.jpg
│   ├── script.txt
│   └── voiceover.mp3
```

## What About Copyright?

**Important:** Only use videos and pictures that are FREE to use!

**Safe sources (all free):**
- Pexels
- Pixabay
- Unsplash
- Coverr

**NOT safe (don't use!):**
- Random Google images
- Other people's YouTube videos
- Movie clips
- TV show clips

Using copyrighted stuff can get your video deleted or your channel banned!

## Your Assignment!

Before Module 6:

1. **Get your Pexels API key**
2. **Run the video_finder.py script** with different search terms
3. **Download at least 10 video clips** related to your channel topic
4. **Download at least 10 pictures** too
5. **Organize them in folders**

## Key Words to Remember

| Word | What It Means |
|------|---------------|
| Stock Footage | Pre-made video clips you can use |
| API | A way for programs to talk to websites |
| API Key | Your personal password for using an API |
| Landscape | Wide format (good for YouTube) |
| Portrait | Tall format (like phone videos) |
| Copyright | Legal ownership of content |

## Quick Quiz!

1. Name 2 websites where you can get free videos
2. What is an API key?
3. Why should you use landscape videos?
4. Why can't you use random Google images?

---

## Achievement Unlocked!

**"Visual Hunter"** - You can now find free videos and pictures!

**Progress: Module 5 of 12 Complete!**

Next up: Module 6 - Putting Your Video Together! You'll learn to combine everything into a real video!
