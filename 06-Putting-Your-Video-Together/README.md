# Module 6: Putting Your Video Together!

## Hey Krwutarth! Let's Build Your First Video!

This is where the magic happens! You've got your script, your voiceover, and your video clips. Now let's combine them into an AWESOME YouTube video!

## What is Video Editing?

**Video editing** = Putting different pieces together to make one complete video.

Think of it like building with LEGO blocks:
- Your voiceover is one block
- Each video clip is another block
- Pictures are blocks too
- You stack them together to build something cool!

## Two Ways to Edit Videos

### Option 1: Free Software (Manual Editing)
- **DaVinci Resolve** - Professional and FREE!
- **Kdenlive** - Simple and FREE!
- **CapCut** - Easy for beginners!

### Option 2: Python Scripts (Automatic!)
- **MoviePy** - Let code do the work!
- This is what we'll focus on!

## Why Use Python for Video Editing?

With Python, you can:
- Make videos automatically
- Create 10 videos while you sleep!
- No clicking around in software
- Same quality every time

## Your First Video with Python!

Let's create a simple video that combines your voiceover with video clips!

### Step 1: Create the Video Maker Script

1. Open Notepad
2. Copy and paste this code:

```python
"""
Krwutarth's Video Maker!
Combine voiceover + video clips into a YouTube video!
"""

from moviepy.editor import *
import os

def create_simple_video(voiceover_file, video_clips, output_file):
    """
    Create a video by combining voiceover with video clips!
    
    voiceover_file: Your MP3 voiceover
    video_clips: List of video file paths
    output_file: Name for your final video
    """
    
    print("=" * 50)
    print("KRWUTARTH'S VIDEO MAKER")
    print("=" * 50)
    print()
    
    # Step 1: Load the voiceover
    print("Loading voiceover...")
    audio = AudioFileClip(voiceover_file)
    total_duration = audio.duration
    print(f"Voiceover length: {total_duration:.1f} seconds")
    print()
    
    # Step 2: Load and prepare video clips
    print("Loading video clips...")
    clips = []
    
    for clip_path in video_clips:
        if os.path.exists(clip_path):
            print(f"  Loading: {clip_path}")
            clip = VideoFileClip(clip_path)
            clips.append(clip)
        else:
            print(f"  Not found: {clip_path}")
    
    if not clips:
        print("ERROR: No video clips found!")
        return
    
    print(f"Loaded {len(clips)} clips!")
    print()
    
    # Step 3: Calculate how long each clip should be
    clip_duration = total_duration / len(clips)
    print(f"Each clip will be {clip_duration:.1f} seconds")
    print()
    
    # Step 4: Trim clips to the right length
    print("Trimming clips...")
    trimmed_clips = []
    
    for i, clip in enumerate(clips):
        # If clip is shorter than needed, loop it
        if clip.duration < clip_duration:
            clip = clip.loop(duration=clip_duration)
        else:
            clip = clip.subclip(0, clip_duration)
        
        # Resize to 1920x1080 (Full HD)
        clip = clip.resize((1920, 1080))
        
        trimmed_clips.append(clip)
        print(f"  Clip {i+1}: Ready!")
    
    print()
    
    # Step 5: Combine all clips
    print("Combining clips...")
    final_video = concatenate_videoclips(trimmed_clips)
    
    # Step 6: Add the voiceover
    print("Adding voiceover...")
    final_video = final_video.set_audio(audio)
    
    # Step 7: Export the video
    print()
    print("Creating your video... (this may take a few minutes)")
    print()
    
    final_video.write_videofile(
        output_file,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        threads=4
    )
    
    # Clean up
    audio.close()
    for clip in clips:
        clip.close()
    final_video.close()
    
    print()
    print("=" * 50)
    print(f"VIDEO COMPLETE: {output_file}")
    print("=" * 50)

# === MAIN PROGRAM ===
if __name__ == "__main__":
    
    # Your voiceover file
    voiceover = "my_voiceover.mp3"
    
    # Your video clips (add your own files here!)
    videos = [
        "downloads/video_1.mp4",
        "downloads/video_2.mp4",
        "downloads/video_3.mp4",
    ]
    
    # Output file name
    output = "my_first_youtube_video.mp4"
    
    # Create the video!
    create_simple_video(voiceover, videos, output)
    
    input("Press Enter to close...")
```

3. Save it as `video_maker.py`

### Step 2: Prepare Your Files

Make sure you have:
- A voiceover file (from Module 4)
- Some video clips (from Module 5)

Update the file paths in the script to match YOUR files!

### Step 3: Run It!

1. Open Command Prompt
2. Type: `python video_maker.py`
3. Wait (this takes a few minutes)
4. Check for your new video!

## Adding Text to Your Videos!

Want to add titles or text? Here's how:

```python
"""
Krwutarth's Video Maker with Text!
Add cool titles to your videos!
"""

from moviepy.editor import *

def create_title_card(text, duration=3, size=(1920, 1080)):
    """Create a title screen with text"""
    
    # Create text clip
    txt_clip = TextClip(
        text,
        fontsize=70,
        color='white',
        font='Arial-Bold',
        size=size,
        method='caption'
    )
    
    # Center the text
    txt_clip = txt_clip.set_position('center')
    txt_clip = txt_clip.set_duration(duration)
    
    # Create black background
    bg_clip = ColorClip(size=size, color=(0, 0, 0))
    bg_clip = bg_clip.set_duration(duration)
    
    # Combine text and background
    title_card = CompositeVideoClip([bg_clip, txt_clip])
    
    return title_card

def create_video_with_titles(voiceover, video_clips, output, title_text):
    """Create a video with a title card at the start"""
    
    print("Creating video with title...")
    
    # Load audio
    audio = AudioFileClip(voiceover)
    
    # Create title card (3 seconds)
    title = create_title_card(title_text, duration=3)
    
    # Load video clips
    clips = [title]  # Start with title
    
    remaining_duration = audio.duration - 3  # Subtract title time
    clip_duration = remaining_duration / len(video_clips)
    
    for clip_path in video_clips:
        clip = VideoFileClip(clip_path)
        if clip.duration < clip_duration:
            clip = clip.loop(duration=clip_duration)
        else:
            clip = clip.subclip(0, clip_duration)
        clip = clip.resize((1920, 1080))
        clips.append(clip)
    
    # Combine everything
    final = concatenate_videoclips(clips)
    final = final.set_audio(audio)
    
    # Export
    final.write_videofile(output, fps=30)
    
    print(f"Done! Video saved as: {output}")

# Example usage
if __name__ == "__main__":
    create_video_with_titles(
        voiceover="my_voiceover.mp3",
        video_clips=["downloads/video_1.mp4", "downloads/video_2.mp4"],
        output="video_with_title.mp4",
        title_text="5 Amazing Facts\nAbout Sharks!"
    )
```

## Adding Background Music!

Want some music playing softly behind your voice? Here's how:

```python
"""
Add background music to your video!
"""

from moviepy.editor import *

def add_background_music(video_file, music_file, output_file, music_volume=0.1):
    """
    Add background music to a video.
    music_volume: How loud the music is (0.1 = 10% volume)
    """
    
    print("Adding background music...")
    
    # Load the video
    video = VideoFileClip(video_file)
    
    # Load the music
    music = AudioFileClip(music_file)
    
    # Make music the same length as video
    if music.duration < video.duration:
        music = music.loop(duration=video.duration)
    else:
        music = music.subclip(0, video.duration)
    
    # Make music quieter
    music = music.volumex(music_volume)
    
    # Combine original audio with music
    original_audio = video.audio
    combined_audio = CompositeAudioClip([original_audio, music])
    
    # Set the new audio
    final_video = video.set_audio(combined_audio)
    
    # Export
    final_video.write_videofile(output_file, fps=30)
    
    print(f"Done! Saved as: {output_file}")

# Example
add_background_music(
    video_file="my_video.mp4",
    music_file="background_music.mp3",
    output_file="video_with_music.mp4",
    music_volume=0.15  # 15% volume
)
```

## Video Editing Tips

### 1. Keep Clips Short
Change clips every 5-10 seconds to keep viewers interested!

### 2. Match Visuals to Words
When you say "shark," show a shark!

### 3. Use Transitions Sparingly
Simple cuts work best. Fancy transitions can be distracting.

### 4. Check Audio Levels
Make sure your voice is louder than background music!

### 5. Export in HD
Always use 1920x1080 resolution for YouTube!

## Common Problems and Fixes

### "MoviePy not found"
Run: `pip install moviepy`

### "Video is too slow to create"
- Use fewer clips
- Lower the resolution temporarily for testing
- Be patient - video creation takes time!

### "Audio doesn't match video"
Make sure your voiceover length matches your total clip length!

### "Video looks blurry"
Make sure you're using HD video clips (at least 1280x720)

## Your Assignment!

Before Module 7:

1. **Create your first video** using the video_maker.py script
2. **Add a title card** to the beginning
3. **Watch your video** - does it look good?
4. **Make adjustments** if needed

## Key Words to Remember

| Word | What It Means |
|------|---------------|
| Clip | A piece of video |
| Concatenate | Join clips together |
| Resolution | Video size (1920x1080 = Full HD) |
| FPS | Frames per second (30 is standard) |
| Codec | How video is compressed |
| Export | Save your final video |

## Quick Quiz!

1. What does MoviePy do?
2. What resolution should YouTube videos be?
3. How do you make background music quieter?
4. Why should you keep clips short?

---

## Achievement Unlocked!

**"Video Creator"** - You can now create complete videos!

**Progress: Module 6 of 12 Complete!**

Next up: Module 7 - Setting Up Your YouTube Channel! Time to go live!
