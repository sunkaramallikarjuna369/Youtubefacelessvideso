# Module 9: The Auto-Magic Video Maker!

## Hey Krwutarth! Let's Automate EVERYTHING!

This is where it gets REALLY cool! Instead of doing each step manually, we're going to create a magic machine that does EVERYTHING for you - from writing the script to creating the final video!

## What is Automation?

**Automation** = Making the computer do work for you automatically!

Instead of:
1. Writing a script (5 minutes)
2. Creating voiceover (2 minutes)
3. Finding videos (10 minutes)
4. Editing video (20 minutes)

You just:
1. Run ONE program (1 minute)
2. Wait (10 minutes)
3. Done! Video ready!

## The Complete Video Pipeline

Here's what our automation will do:

```
Topic → Script → Voiceover → Videos → Final Video → Thumbnail → Metadata
```

All automatically! Like magic!

## The Ultimate Video Generator Script

This is the BIG one! Save this script and you can create videos with just ONE command!

```python
"""
KRWUTARTH'S ULTIMATE VIDEO GENERATOR!
Create complete YouTube videos automatically!

Just give it a topic, and it does EVERYTHING:
1. Writes the script using AI
2. Creates the voiceover
3. Downloads video clips
4. Assembles the video
5. Creates a thumbnail
6. Generates title, description, and tags

HOW TO USE:
1. Make sure Ollama is running (ollama serve)
2. Run this script
3. Enter your topic
4. Wait for magic to happen!
"""

import os
import asyncio
import requests
import edge_tts
from datetime import datetime

# Try to import video libraries
try:
    from moviepy.editor import *
    MOVIEPY_AVAILABLE = True
except:
    MOVIEPY_AVAILABLE = False
    print("Note: MoviePy not installed. Video assembly will be skipped.")

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except:
    PILLOW_AVAILABLE = False

# === CONFIGURATION ===
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"  # Get from pexels.com/api
VOICE = "en-US-GuyNeural"  # Change voice if you want

class VideoGenerator:
    """The Ultimate Video Generator for Krwutarth!"""
    
    def __init__(self, topic, num_points=5):
        self.topic = topic
        self.num_points = num_points
        self.project_folder = self.create_project_folder()
        
    def create_project_folder(self):
        """Create a folder for this video project"""
        # Create unique folder name with date
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() else "_" for c in self.topic[:30])
        folder_name = f"project_{date_str}_{safe_topic}"
        
        os.makedirs(folder_name, exist_ok=True)
        os.makedirs(f"{folder_name}/videos", exist_ok=True)
        
        print(f"Created project folder: {folder_name}")
        return folder_name
    
    def generate_script(self):
        """Use AI to write the video script"""
        print("\n" + "=" * 50)
        print("STEP 1: Writing Script with AI...")
        print("=" * 50)
        
        prompt = f"""Write a fun, engaging YouTube video script about: {self.topic}

The script should:
- Start with an exciting hook (first 5 seconds)
- Have {self.num_points} main points
- Be written for kids and teenagers
- Sound natural and exciting, not boring!
- Be about 2 minutes long when read aloud
- End with a call to action (subscribe, like)

Make it fun and easy to understand!"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            
            script = response.json().get('response', '')
            
            # Save script
            script_file = f"{self.project_folder}/script.txt"
            with open(script_file, "w", encoding="utf-8") as f:
                f.write(script)
            
            print(f"Script saved to: {script_file}")
            print(f"Script length: {len(script)} characters")
            
            return script
            
        except requests.exceptions.ConnectionError:
            print("ERROR: Ollama not running! Start it with: ollama serve")
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    async def generate_voiceover(self, script):
        """Convert script to speech"""
        print("\n" + "=" * 50)
        print("STEP 2: Creating Voiceover...")
        print("=" * 50)
        
        output_file = f"{self.project_folder}/voiceover.mp3"
        
        communicate = edge_tts.Communicate(script, VOICE)
        await communicate.save(output_file)
        
        print(f"Voiceover saved to: {output_file}")
        return output_file
    
    def download_videos(self, search_terms, num_videos=5):
        """Download stock videos from Pexels"""
        print("\n" + "=" * 50)
        print("STEP 3: Downloading Video Clips...")
        print("=" * 50)
        
        if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
            print("WARNING: No Pexels API key set!")
            print("Get one free at: https://www.pexels.com/api/")
            return []
        
        downloaded = []
        
        for term in search_terms[:3]:  # Search for 3 terms
            print(f"Searching for: {term}")
            
            try:
                response = requests.get(
                    "https://api.pexels.com/videos/search",
                    headers={"Authorization": PEXELS_API_KEY},
                    params={
                        "query": term,
                        "per_page": 2,
                        "orientation": "landscape"
                    }
                )
                
                if response.status_code == 200:
                    videos = response.json().get("videos", [])
                    
                    for video in videos:
                        video_files = video.get("video_files", [])
                        
                        # Find HD version
                        for vf in video_files:
                            if vf.get("quality") == "hd":
                                video_url = vf.get("link")
                                video_id = video.get("id")
                                filename = f"{self.project_folder}/videos/clip_{video_id}.mp4"
                                
                                print(f"  Downloading video {video_id}...")
                                
                                vid_response = requests.get(video_url, stream=True)
                                with open(filename, "wb") as f:
                                    for chunk in vid_response.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                
                                downloaded.append(filename)
                                break
                                
            except Exception as e:
                print(f"  Error: {e}")
        
        print(f"Downloaded {len(downloaded)} video clips!")
        return downloaded
    
    def assemble_video(self, voiceover_file, video_clips):
        """Combine voiceover and video clips"""
        print("\n" + "=" * 50)
        print("STEP 4: Assembling Video...")
        print("=" * 50)
        
        if not MOVIEPY_AVAILABLE:
            print("MoviePy not available. Skipping video assembly.")
            return None
        
        if not video_clips:
            print("No video clips to assemble!")
            return None
        
        output_file = f"{self.project_folder}/final_video.mp4"
        
        try:
            # Load audio
            audio = AudioFileClip(voiceover_file)
            duration = audio.duration
            
            # Load and prepare clips
            clips = []
            clip_duration = duration / len(video_clips)
            
            for clip_path in video_clips:
                clip = VideoFileClip(clip_path)
                
                if clip.duration < clip_duration:
                    clip = clip.loop(duration=clip_duration)
                else:
                    clip = clip.subclip(0, clip_duration)
                
                clip = clip.resize((1920, 1080))
                clips.append(clip)
            
            # Combine clips
            final = concatenate_videoclips(clips)
            final = final.set_audio(audio)
            
            # Export
            print("Rendering video... (this may take a few minutes)")
            final.write_videofile(
                output_file,
                fps=30,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Cleanup
            audio.close()
            for clip in clips:
                clip.close()
            final.close()
            
            print(f"Video saved to: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"Error assembling video: {e}")
            return None
    
    def create_thumbnail(self):
        """Create a thumbnail for the video"""
        print("\n" + "=" * 50)
        print("STEP 5: Creating Thumbnail...")
        print("=" * 50)
        
        if not PILLOW_AVAILABLE:
            print("Pillow not available. Skipping thumbnail.")
            return None
        
        output_file = f"{self.project_folder}/thumbnail.jpg"
        
        # Create thumbnail
        width, height = 1280, 720
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Gradient background
        for y in range(height):
            r = int(200 - (y / height) * 150)
            g = int(50 + (y / height) * 50)
            b = int(50 + (y / height) * 100)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        # Shorten topic for thumbnail
        short_topic = self.topic[:40] + "..." if len(self.topic) > 40 else self.topic
        
        # Draw text with outline
        text_y = height // 2 - 50
        for dx, dy in [(-3,-3), (-3,3), (3,-3), (3,3)]:
            draw.text((width//2 + dx, text_y + dy), short_topic, 
                     font=font, fill=(0,0,0), anchor="mm")
        draw.text((width//2, text_y), short_topic, 
                 font=font, fill=(255,255,0), anchor="mm")
        
        img.save(output_file, quality=95)
        print(f"Thumbnail saved to: {output_file}")
        return output_file
    
    def generate_metadata(self):
        """Generate title, description, and tags"""
        print("\n" + "=" * 50)
        print("STEP 6: Generating Metadata...")
        print("=" * 50)
        
        # Generate title
        title = f"{self.num_points} AMAZING Facts About {self.topic}!"
        
        # Generate description
        description = f"""In this video, you'll discover {self.num_points} incredible facts about {self.topic}!

If you enjoyed this video, please LIKE and SUBSCRIBE!
Turn on notifications so you never miss a video!

#facts #{self.topic.replace(' ', '').lower()} #amazing #educational
"""
        
        # Generate tags
        tags = [
            self.topic,
            f"{self.topic} facts",
            f"amazing {self.topic}",
            "facts",
            "amazing facts",
            "did you know",
            "educational",
            "for kids"
        ]
        
        # Save metadata
        metadata_file = f"{self.project_folder}/metadata.txt"
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write(f"TITLE:\n{title}\n\n")
            f.write(f"DESCRIPTION:\n{description}\n\n")
            f.write(f"TAGS:\n{', '.join(tags)}\n")
        
        print(f"Title: {title}")
        print(f"Metadata saved to: {metadata_file}")
        
        return title, description, tags
    
    async def generate_complete_video(self):
        """Run the complete video generation pipeline!"""
        print("\n" + "=" * 60)
        print("KRWUTARTH'S ULTIMATE VIDEO GENERATOR")
        print("=" * 60)
        print(f"Topic: {self.topic}")
        print(f"Points: {self.num_points}")
        print("=" * 60)
        
        # Step 1: Generate script
        script = self.generate_script()
        if not script:
            print("Failed to generate script!")
            return
        
        # Step 2: Create voiceover
        voiceover = await self.generate_voiceover(script)
        
        # Step 3: Download videos
        search_terms = [self.topic] + self.topic.split()[:2]
        video_clips = self.download_videos(search_terms)
        
        # Step 4: Assemble video
        if video_clips:
            self.assemble_video(voiceover, video_clips)
        
        # Step 5: Create thumbnail
        self.create_thumbnail()
        
        # Step 6: Generate metadata
        self.generate_metadata()
        
        print("\n" + "=" * 60)
        print("VIDEO GENERATION COMPLETE!")
        print("=" * 60)
        print(f"All files saved in: {self.project_folder}")
        print("\nFiles created:")
        for f in os.listdir(self.project_folder):
            print(f"  - {f}")
        print("=" * 60)


# === MAIN PROGRAM ===
if __name__ == "__main__":
    print("=" * 60)
    print("WELCOME TO KRWUTARTH'S VIDEO GENERATOR!")
    print("=" * 60)
    print()
    
    # Get topic from user
    topic = input("What topic do you want to make a video about? ")
    
    if not topic:
        topic = "Amazing Ocean Animals"  # Default topic
    
    # Create generator and run!
    generator = VideoGenerator(topic, num_points=5)
    asyncio.run(generator.generate_complete_video())
    
    print()
    input("Press Enter to close...")
```

## How to Use the Video Generator

### Step 1: Set Up Your API Key

Find this line in the code:
```python
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"
```

Replace it with your actual Pexels API key!

### Step 2: Make Sure Ollama is Running

Open a Command Prompt and type:
```
ollama serve
```

Leave this window open!

### Step 3: Run the Generator

Open another Command Prompt in your youtube-videos folder:
```
python video_generator.py
```

### Step 4: Enter Your Topic

When it asks "What topic?", type something like:
- "Amazing Shark Facts"
- "Cool Space Discoveries"
- "Minecraft Building Tips"

### Step 5: Wait for Magic!

The program will:
1. Write a script (30-60 seconds)
2. Create voiceover (10 seconds)
3. Download videos (1-2 minutes)
4. Assemble video (2-5 minutes)
5. Create thumbnail (instant)
6. Generate metadata (instant)

## Batch Video Generator

Want to create MULTIPLE videos at once? Here's how:

```python
"""
Krwutarth's Batch Video Generator!
Create multiple videos automatically!
"""

import asyncio
from video_generator import VideoGenerator

async def create_multiple_videos(topics):
    """Create videos for multiple topics"""
    
    print("=" * 60)
    print("BATCH VIDEO GENERATOR")
    print(f"Creating {len(topics)} videos!")
    print("=" * 60)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n>>> VIDEO {i} of {len(topics)}: {topic}")
        
        generator = VideoGenerator(topic, num_points=5)
        await generator.generate_complete_video()
        
        print(f">>> VIDEO {i} COMPLETE!")
    
    print("\n" + "=" * 60)
    print("ALL VIDEOS COMPLETE!")
    print("=" * 60)

# List of topics to create videos about
my_topics = [
    "5 Amazing Facts About Sharks",
    "10 Cool Things About Space",
    "Why Dinosaurs Went Extinct",
]

# Run the batch generator
asyncio.run(create_multiple_videos(my_topics))
```

## Tips for Better Automated Videos

### 1. Choose Good Topics
The AI works best with clear, specific topics!

### 2. Check the Output
Always watch your video before uploading to make sure it looks good!

### 3. Edit if Needed
Sometimes you might want to make small changes manually.

### 4. Keep Your API Keys Safe
Don't share your API keys with anyone!

## Your Assignment!

Before Module 10:

1. **Save the video generator script**
2. **Add your Pexels API key**
3. **Generate your first automated video**
4. **Watch it and see how it looks!**
5. **Try generating 3 different videos**

## Key Words to Remember

| Word | What It Means |
|------|---------------|
| Automation | Making computers do work automatically |
| Pipeline | A series of steps that run in order |
| Batch | Doing multiple things at once |
| API Key | Your password for using online services |

## Quick Quiz!

1. What does the video generator do automatically?
2. Why do you need to run "ollama serve" first?
3. What is a "batch" video generator?
4. Why should you watch your video before uploading?

---

## Achievement Unlocked!

**"Automation Wizard"** - You can now create videos automatically!

**Progress: Module 9 of 12 Complete!**

Next up: Module 10 - Uploading Videos Automatically! Put your videos on YouTube without clicking!
