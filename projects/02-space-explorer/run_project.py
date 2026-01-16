"""
KRWUTARTH'S SPACE EXPLORER VIDEO GENERATOR!

This script creates a complete YouTube video about space!
Just run it and watch the magic happen!
"""

import os
import sys
import asyncio
import requests
from datetime import datetime

try:
    import edge_tts
except ImportError:
    os.system("pip install edge-tts")
    import edge_tts

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

from config import *


def print_banner():
    print("\n" + "=" * 60)
    print("   KRWUTARTH'S SPACE EXPLORER VIDEO GENERATOR!")
    print("=" * 60 + "\n")


def check_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def generate_script():
    print("[STEP 1] Writing script with AI...")
    print(f"  Topic: {TOPIC}\n")
    
    prompt = f"""Write a fun, engaging YouTube video script about: {TOPIC}

The script should:
- Start with an exciting hook like "Have you ever wondered what's out there in space?"
- Have exactly {NUM_FACTS} amazing facts about space
- Be written for kids and teenagers (fun and easy to understand!)
- Sound natural and exciting, not boring
- Be about 2 minutes long when read aloud
- End with "If you enjoyed this video, smash that subscribe button!"

Make it super interesting! Use phrases like "Did you know..." and "Here's something mind-blowing..."
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
            timeout=120
        )
        script = response.json().get('response', '')
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        with open(os.path.join(OUTPUT_FOLDER, "script.txt"), "w", encoding="utf-8") as f:
            f.write(script)
        print(f"  Script saved! Length: {len(script)} characters\n")
        return script
    except requests.exceptions.ConnectionError:
        print("  ERROR: Ollama is not running! Type: ollama serve")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


async def generate_voiceover(script):
    print("[STEP 2] Creating voiceover...")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = os.path.join(OUTPUT_FOLDER, "voiceover.mp3")
    try:
        communicate = edge_tts.Communicate(script, VOICE)
        await communicate.save(output_file)
        print(f"  Voiceover saved to: {output_file}\n")
        return output_file
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def download_videos():
    print("[STEP 3] Downloading video clips...")
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("  WARNING: No Pexels API key! Get one at: https://www.pexels.com/api/")
        return []
    
    os.makedirs(os.path.join(OUTPUT_FOLDER, "clips"), exist_ok=True)
    downloaded = []
    
    for term in VIDEO_SEARCH_TERMS[:3]:
        print(f"  Searching for: {term}")
        try:
            response = requests.get(
                "https://api.pexels.com/videos/search",
                headers={"Authorization": PEXELS_API_KEY},
                params={"query": term, "per_page": 2, "orientation": "landscape"}
            )
            if response.status_code == 200:
                for video in response.json().get("videos", [])[:2]:
                    for vf in video.get("video_files", []):
                        if vf.get("quality") == "hd" and vf.get("width", 0) >= 1280:
                            filename = os.path.join(OUTPUT_FOLDER, "clips", f"clip_{video.get('id')}.mp4")
                            print(f"    Downloading video {video.get('id')}...")
                            vid_response = requests.get(vf.get("link"), stream=True)
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
    
    print(f"  Downloaded {len(downloaded)} clips!\n")
    return downloaded


def assemble_video(voiceover_file, video_clips):
    print("[STEP 4] Assembling video...")
    if not MOVIEPY_AVAILABLE or not video_clips:
        print("  Skipping video assembly.\n")
        return None
    
    output_file = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    try:
        audio = AudioFileClip(voiceover_file)
        duration = audio.duration
        clips = []
        clip_duration = duration / len(video_clips)
        
        for clip_path in video_clips:
            if os.path.exists(clip_path):
                clip = VideoFileClip(clip_path)
                if clip.duration < clip_duration:
                    clip = clip.loop(duration=clip_duration)
                else:
                    clip = clip.subclip(0, clip_duration)
                clip = clip.resize((1920, 1080))
                clips.append(clip)
        
        if clips:
            final = concatenate_videoclips(clips)
            final = final.set_audio(audio)
            print("  Rendering video...")
            final.write_videofile(output_file, fps=30, codec='libx264', audio_codec='aac', threads=4, logger=None)
            audio.close()
            for clip in clips:
                clip.close()
            final.close()
            print(f"  Video saved to: {output_file}\n")
            return output_file
    except Exception as e:
        print(f"  ERROR: {e}")
    return None


def create_thumbnail():
    print("[STEP 5] Creating thumbnail...")
    if not PILLOW_AVAILABLE:
        return None
    
    output_file = os.path.join(OUTPUT_FOLDER, "thumbnail.jpg")
    try:
        width, height = 1280, 720
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        for y in range(height):
            r = int(10 + (y / height) * 40)
            g = int(10 + (y / height) * 10)
            b = int(50 + (y / height) * 50)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        try:
            font = ImageFont.truetype("arial.ttf", 90)
            small_font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        for dx, dy in [(-3,-3), (-3,3), (3,-3), (3,3)]:
            draw.text((width//2 + dx, height//2 - 50 + dy), THUMBNAIL_TEXT, font=font, fill=(0,0,0), anchor="mm")
        draw.text((width//2, height//2 - 50), THUMBNAIL_TEXT, font=font, fill=(255,255,0), anchor="mm")
        draw.text((width//2, height//2 + 50), THUMBNAIL_SUBTITLE, font=small_font, fill=(255,255,255), anchor="mm")
        
        img.save(output_file, quality=95)
        print(f"  Thumbnail saved to: {output_file}\n")
        return output_file
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def generate_metadata():
    print("[STEP 6] Generating metadata...")
    title = f"{NUM_FACTS} MIND-BLOWING Space Facts That Will AMAZE You!"
    description = f"""In this video, you'll discover {NUM_FACTS} incredible facts about space!

Space is full of mysteries and amazing discoveries. From distant galaxies to black holes, there's so much to explore!

If you enjoyed this video, please LIKE and SUBSCRIBE!

#space #spacefacts #astronomy #universe #planets #stars #science #educational
"""
    tags = ["space facts", "astronomy", "universe", "planets", "stars", "galaxy", "science", "educational"]
    
    with open(os.path.join(OUTPUT_FOLDER, "metadata.txt"), "w", encoding="utf-8") as f:
        f.write(f"TITLE:\n{title}\n\nDESCRIPTION:\n{description}\n\nTAGS:\n{', '.join(tags)}\n")
    print(f"  Title: {title}\n")
    return title, description, tags


async def main():
    print_banner()
    if not check_ollama():
        print("ERROR: Ollama is not running! Type: ollama serve")
        input("\nPress Enter to close...")
        return
    
    script = generate_script()
    if not script:
        input("\nPress Enter to close...")
        return
    
    voiceover = await generate_voiceover(script)
    if not voiceover:
        input("\nPress Enter to close...")
        return
    
    video_clips = download_videos()
    if video_clips and MOVIEPY_AVAILABLE:
        assemble_video(voiceover, video_clips)
    
    create_thumbnail()
    generate_metadata()
    
    print("=" * 60)
    print("   VIDEO GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nAll files saved in: {OUTPUT_FOLDER}/")
    print("\nGreat job, Krwutarth! You just created a space video!\n")
    input("Press Enter to close...")


if __name__ == "__main__":
    asyncio.run(main())
