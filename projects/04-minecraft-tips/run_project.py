"""
KRWUTARTH'S MINECRAFT TIPS VIDEO GENERATOR!
"""

import os
import asyncio
import requests

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
    print("   KRWUTARTH'S MINECRAFT TIPS VIDEO GENERATOR!")
    print("=" * 60 + "\n")

def check_ollama():
    try:
        return requests.get("http://localhost:11434/api/tags", timeout=5).status_code == 200
    except:
        return False

def generate_script():
    print("[STEP 1] Writing script with AI...")
    prompt = f"""Write a fun YouTube video script about: {TOPIC}

The script should:
- Start with "Hey gamers! Want to become a Minecraft pro?"
- Have exactly {NUM_FACTS} awesome Minecraft tips
- Be written for kids who love gaming
- Be about 2 minutes long
- End with "Subscribe for more gaming tips!"

Make it exciting and use gaming language!"""

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
    except:
        print("  ERROR: Ollama not running! Type: ollama serve")
        return None

async def generate_voiceover(script):
    print("[STEP 2] Creating voiceover...")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = os.path.join(OUTPUT_FOLDER, "voiceover.mp3")
    try:
        await edge_tts.Communicate(script, VOICE).save(output_file)
        print(f"  Voiceover saved!\n")
        return output_file
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def download_videos():
    print("[STEP 3] Downloading video clips...")
    if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
        print("  WARNING: No Pexels API key!")
        return []
    
    os.makedirs(os.path.join(OUTPUT_FOLDER, "clips"), exist_ok=True)
    downloaded = []
    
    for term in VIDEO_SEARCH_TERMS[:3]:
        try:
            response = requests.get(
                "https://api.pexels.com/videos/search",
                headers={"Authorization": PEXELS_API_KEY},
                params={"query": term, "per_page": 2, "orientation": "landscape"}
            )
            if response.status_code == 200:
                for video in response.json().get("videos", [])[:2]:
                    for vf in video.get("video_files", []):
                        if vf.get("quality") == "hd":
                            filename = os.path.join(OUTPUT_FOLDER, "clips", f"clip_{video.get('id')}.mp4")
                            vid_response = requests.get(vf.get("link"), stream=True)
                            with open(filename, "wb") as f:
                                for chunk in vid_response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            downloaded.append(filename)
                            break
                    if len(downloaded) >= NUM_VIDEO_CLIPS:
                        break
        except:
            pass
    print(f"  Downloaded {len(downloaded)} clips!\n")
    return downloaded

def assemble_video(voiceover_file, video_clips):
    print("[STEP 4] Assembling video...")
    if not MOVIEPY_AVAILABLE or not video_clips:
        return None
    
    output_file = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    try:
        audio = AudioFileClip(voiceover_file)
        clips = []
        clip_duration = audio.duration / len(video_clips)
        
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
            final = concatenate_videoclips(clips).set_audio(audio)
            final.write_videofile(output_file, fps=30, codec='libx264', audio_codec='aac', threads=4, logger=None)
            audio.close()
            for clip in clips:
                clip.close()
            final.close()
            print(f"  Video saved!\n")
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
        img = Image.new('RGB', (1280, 720))
        draw = ImageDraw.Draw(img)
        for y in range(720):
            draw.line([(0, y), (1280, y)], fill=(int(50 + y/10), int(200 - y/5), int(50)))
        try:
            font = ImageFont.truetype("arial.ttf", 90)
        except:
            font = ImageFont.load_default()
        draw.text((640, 310), THUMBNAIL_TEXT, font=font, fill=(255,255,0), anchor="mm")
        img.save(output_file, quality=95)
        print(f"  Thumbnail saved!\n")
    except:
        pass
    return output_file

def generate_metadata():
    print("[STEP 6] Generating metadata...")
    title = f"{NUM_FACTS} MINECRAFT Tips That Will Make You a PRO!"
    description = f"Learn {NUM_FACTS} pro Minecraft tips!\n\n#minecraft #gaming #tips #tricks"
    tags = ["minecraft", "minecraft tips", "gaming", "minecraft tricks", "minecraft tutorial"]
    with open(os.path.join(OUTPUT_FOLDER, "metadata.txt"), "w") as f:
        f.write(f"TITLE:\n{title}\n\nDESCRIPTION:\n{description}\n\nTAGS:\n{', '.join(tags)}")
    print(f"  Metadata saved!\n")

async def main():
    print_banner()
    if not check_ollama():
        print("ERROR: Ollama not running! Type: ollama serve")
        input("\nPress Enter to close...")
        return
    
    script = generate_script()
    if not script:
        input("\nPress Enter to close...")
        return
    
    voiceover = await generate_voiceover(script)
    if voiceover:
        video_clips = download_videos()
        if video_clips:
            assemble_video(voiceover, video_clips)
        create_thumbnail()
        generate_metadata()
    
    print("=" * 60)
    print("   VIDEO COMPLETE! Check the output folder!")
    print("=" * 60)
    input("\nPress Enter to close...")

if __name__ == "__main__":
    asyncio.run(main())
