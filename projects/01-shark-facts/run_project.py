"""
KRWUTARTH'S SHARK FACTS VIDEO GENERATOR!

This script creates a complete YouTube video about sharks!
Just run it and watch the magic happen!

HOW TO USE:
1. Make sure Ollama is running (ollama serve)
2. Add your Pexels API key in config.py
3. Run: python run_project.py
4. Find your video in the output folder!
"""

import os
import sys
import asyncio
import requests
from datetime import datetime

# Try to import required libraries
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("Installing edge-tts...")
    os.system("pip install edge-tts")
    import edge_tts
    EDGE_TTS_AVAILABLE = True

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("Note: MoviePy not installed. Run: pip install moviepy")

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Note: Pillow not installed. Run: pip install Pillow")

# Import our config
from config import *


def print_banner():
    """Show a cool banner!"""
    print()
    print("=" * 60)
    print("   KRWUTARTH'S SHARK FACTS VIDEO GENERATOR!")
    print("=" * 60)
    print()


def check_ollama():
    """Make sure Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def generate_script():
    """Use AI to write a shark facts script"""
    print("[STEP 1] Writing script with AI...")
    print(f"  Topic: {TOPIC}")
    print()
    
    prompt = f"""Write a fun, engaging YouTube video script about: {TOPIC}

The script should:
- Start with an exciting hook to grab attention in the first 5 seconds
- Have exactly {NUM_FACTS} amazing facts
- Be written for kids and teenagers (fun and easy to understand!)
- Sound natural and exciting, not boring
- Be about 2 minutes long when read aloud
- End with "If you enjoyed this video, smash that subscribe button!"

Make it super interesting and fun! Use phrases like "Did you know..." and "Here's something crazy..."
"""

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
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        script_file = os.path.join(OUTPUT_FOLDER, "script.txt")
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script)
        
        print(f"  Script saved to: {script_file}")
        print(f"  Script length: {len(script)} characters")
        print()
        
        return script
        
    except requests.exceptions.ConnectionError:
        print("  ERROR: Ollama is not running!")
        print("  Open Command Prompt and type: ollama serve")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


async def generate_voiceover(script):
    """Convert script to speech"""
    print("[STEP 2] Creating voiceover...")
    print(f"  Voice: {VOICE}")
    print()
    
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = os.path.join(OUTPUT_FOLDER, "voiceover.mp3")
    
    try:
        communicate = edge_tts.Communicate(script, VOICE)
        await communicate.save(output_file)
        
        print(f"  Voiceover saved to: {output_file}")
        print()
        
        return output_file
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def download_videos():
    """Download shark videos from Pexels"""
    print("[STEP 3] Downloading video clips...")
    print(f"  Search terms: {VIDEO_SEARCH_TERMS}")
    print()
    
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("  WARNING: No Pexels API key!")
        print("  Get your free key at: https://www.pexels.com/api/")
        print("  Then add it to config.py")
        return []
    
    os.makedirs(os.path.join(OUTPUT_FOLDER, "clips"), exist_ok=True)
    downloaded = []
    
    for term in VIDEO_SEARCH_TERMS[:3]:
        print(f"  Searching for: {term}")
        
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
                
                for video in videos[:2]:
                    video_files = video.get("video_files", [])
                    
                    # Find HD version
                    for vf in video_files:
                        if vf.get("quality") == "hd" and vf.get("width", 0) >= 1280:
                            video_url = vf.get("link")
                            video_id = video.get("id")
                            filename = os.path.join(OUTPUT_FOLDER, "clips", f"clip_{video_id}.mp4")
                            
                            print(f"    Downloading video {video_id}...")
                            
                            vid_response = requests.get(video_url, stream=True)
                            with open(filename, "wb") as f:
                                for chunk in vid_response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            
                            downloaded.append(filename)
                            break
                            
                    if len(downloaded) >= NUM_VIDEO_CLIPS:
                        break
                        
            if len(downloaded) >= NUM_VIDEO_CLIPS:
                break
                
        except Exception as e:
            print(f"    Error: {e}")
    
    print(f"  Downloaded {len(downloaded)} video clips!")
    print()
    
    return downloaded


def assemble_video(voiceover_file, video_clips):
    """Combine voiceover and video clips into final video"""
    print("[STEP 4] Assembling video...")
    print()
    
    if not MOVIEPY_AVAILABLE:
        print("  MoviePy not available. Skipping video assembly.")
        print("  Install with: pip install moviepy")
        return None
    
    if not video_clips:
        print("  No video clips to assemble!")
        return None
    
    output_file = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    
    try:
        # Load audio
        audio = AudioFileClip(voiceover_file)
        duration = audio.duration
        print(f"  Voiceover length: {duration:.1f} seconds")
        
        # Load and prepare clips
        clips = []
        clip_duration = duration / len(video_clips)
        
        for clip_path in video_clips:
            if os.path.exists(clip_path):
                clip = VideoFileClip(clip_path)
                
                # Adjust clip length
                if clip.duration < clip_duration:
                    clip = clip.loop(duration=clip_duration)
                else:
                    clip = clip.subclip(0, clip_duration)
                
                # Resize to 1080p
                clip = clip.resize((1920, 1080))
                clips.append(clip)
        
        if not clips:
            print("  No clips loaded!")
            return None
        
        # Combine clips
        print("  Combining clips...")
        final = concatenate_videoclips(clips)
        final = final.set_audio(audio)
        
        # Export
        print("  Rendering video... (this may take a few minutes)")
        final.write_videofile(
            output_file,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            threads=4,
            logger=None
        )
        
        # Cleanup
        audio.close()
        for clip in clips:
            clip.close()
        final.close()
        
        print(f"  Video saved to: {output_file}")
        print()
        
        return output_file
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def create_thumbnail():
    """Create a thumbnail for the video"""
    print("[STEP 5] Creating thumbnail...")
    print()
    
    if not PILLOW_AVAILABLE:
        print("  Pillow not available. Skipping thumbnail.")
        return None
    
    output_file = os.path.join(OUTPUT_FOLDER, "thumbnail.jpg")
    
    try:
        # Create thumbnail
        width, height = 1280, 720
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Blue gradient background (ocean theme)
        for y in range(height):
            r = int(0 + (y / height) * 30)
            g = int(50 + (y / height) * 100)
            b = int(150 + (y / height) * 105)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 90)
            small_font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Main text
        main_text = "SHARK FACTS!"
        
        # Draw text with outline
        for dx, dy in [(-3,-3), (-3,3), (3,-3), (3,3), (-3,0), (3,0), (0,-3), (0,3)]:
            draw.text((width//2 + dx, height//2 - 50 + dy), main_text, 
                     font=font, fill=(0,0,0), anchor="mm")
        draw.text((width//2, height//2 - 50), main_text, 
                 font=font, fill=(255,255,0), anchor="mm")
        
        # Subtitle
        subtitle = "5 Amazing Facts!"
        draw.text((width//2, height//2 + 50), subtitle, 
                 font=small_font, fill=(255,255,255), anchor="mm")
        
        img.save(output_file, quality=95)
        print(f"  Thumbnail saved to: {output_file}")
        print()
        
        return output_file
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def generate_metadata():
    """Generate title, description, and tags"""
    print("[STEP 6] Generating metadata...")
    print()
    
    title = f"{NUM_FACTS} AMAZING Shark Facts That Will BLOW Your Mind!"
    
    description = f"""In this video, you'll discover {NUM_FACTS} incredible facts about sharks!

Sharks are some of the most amazing creatures in the ocean. From their incredible senses to their powerful jaws, there's so much to learn about these fascinating predators!

If you enjoyed this video, please LIKE and SUBSCRIBE!
Turn on notifications so you never miss a video!

#sharks #sharkfacts #ocean #animals #facts #educational #wildlife #marinelife
"""
    
    tags = [
        "shark facts",
        "sharks",
        "ocean animals",
        "marine life",
        "amazing facts",
        "did you know",
        "educational",
        "wildlife",
        "sea creatures",
        "shark documentary"
    ]
    
    # Save metadata
    metadata_file = os.path.join(OUTPUT_FOLDER, "metadata.txt")
    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write(f"TITLE:\n{title}\n\n")
        f.write(f"DESCRIPTION:\n{description}\n\n")
        f.write(f"TAGS:\n{', '.join(tags)}\n")
    
    print(f"  Title: {title}")
    print(f"  Metadata saved to: {metadata_file}")
    print()
    
    return title, description, tags


async def main():
    """Run the complete video generation pipeline!"""
    print_banner()
    
    # Check Ollama
    if not check_ollama():
        print("ERROR: Ollama is not running!")
        print("Please open Command Prompt and type: ollama serve")
        print("Then run this script again.")
        input("\nPress Enter to close...")
        return
    
    print("Ollama is running! Let's create your video!")
    print()
    
    # Step 1: Generate script
    script = generate_script()
    if not script:
        print("Failed to generate script!")
        input("\nPress Enter to close...")
        return
    
    # Step 2: Create voiceover
    voiceover = await generate_voiceover(script)
    if not voiceover:
        print("Failed to create voiceover!")
        input("\nPress Enter to close...")
        return
    
    # Step 3: Download videos
    video_clips = download_videos()
    
    # Step 4: Assemble video
    if video_clips and MOVIEPY_AVAILABLE:
        assemble_video(voiceover, video_clips)
    
    # Step 5: Create thumbnail
    create_thumbnail()
    
    # Step 6: Generate metadata
    generate_metadata()
    
    # Done!
    print("=" * 60)
    print("   VIDEO GENERATION COMPLETE!")
    print("=" * 60)
    print()
    print(f"All files saved in: {OUTPUT_FOLDER}/")
    print()
    print("Files created:")
    if os.path.exists(OUTPUT_FOLDER):
        for f in os.listdir(OUTPUT_FOLDER):
            print(f"  - {f}")
    print()
    print("Next steps:")
    print("1. Watch your video to make sure it looks good")
    print("2. Upload to YouTube!")
    print("3. Use the metadata.txt for title, description, and tags")
    print()
    print("Great job, Krwutarth! You just created a YouTube video!")
    print()
    input("Press Enter to close...")


if __name__ == "__main__":
    asyncio.run(main())
