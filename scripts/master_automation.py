#!/usr/bin/env python3
"""
MASTER AUTOMATION SCRIPT
Complete Faceless YouTube Video Generation Pipeline

This script automates the entire process from topic to uploaded video:
1. Generate video topic ideas
2. Write script with AI
3. Generate voiceover
4. Download stock footage
5. Assemble video
6. Create thumbnail
7. Generate metadata
8. Upload to YouTube (optional)

Requirements:
pip install edge-tts moviepy Pillow requests python-dotenv google-generativeai

Usage:
python master_automation.py --topic "Your Video Topic" --length 8

Author: Faceless YouTube Automation Course
"""

import os
import sys
import json
import asyncio
import argparse
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FacelessVideoGenerator:
    """
    Complete automation pipeline for faceless YouTube videos.
    100% FREE tools - no paid subscriptions required!
    """
    
    def __init__(self, project_name=None):
        """Initialize the video generator"""
        
        # Generate project name if not provided
        if project_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"video_{timestamp}"
        
        self.project_name = project_name
        self.base_dir = Path("projects") / project_name
        
        # Create directory structure
        self.dirs = {
            'scripts': self.base_dir / 'scripts',
            'voiceovers': self.base_dir / 'voiceovers',
            'footage': self.base_dir / 'footage',
            'thumbnails': self.base_dir / 'thumbnails',
            'output': self.base_dir / 'output',
            'metadata': self.base_dir / 'metadata'
        }
        
        for directory in self.dirs.values():
            directory.mkdir(parents=True, exist_ok=True)
        
        # Configuration
        self.config = {
            'voice': 'en-US-GuyNeural',
            'width': 1920,
            'height': 1080,
            'fps': 30
        }
        
        print(f"[INIT] Project: {self.project_name}")
        print(f"[INIT] Directory: {self.base_dir}")
    
    # ==================== SCRIPT GENERATION ====================
    
    def generate_script(self, topic, length_minutes=8, use_ollama=True):
        """
        Generate a video script using AI
        
        Args:
            topic: Video topic
            length_minutes: Target video length
            use_ollama: Use local Ollama (True) or Gemini API (False)
        """
        print(f"\n[SCRIPT] Generating script for: {topic}")
        
        word_count = length_minutes * 150
        
        prompt = f"""Write a YouTube video script about: {topic}

Requirements:
- Approximately {word_count} words ({length_minutes} minutes when spoken)
- Start with an attention-grabbing hook (first 30 seconds)
- Include 4-5 main sections with clear transitions
- End with a strong call to action (subscribe, like, comment)
- Conversational, engaging tone
- No stage directions or narrator notes - just the spoken words

Write the complete script now:"""

        script = None
        
        if use_ollama:
            script = self._generate_with_ollama(prompt)
        
        if script is None:
            script = self._generate_with_gemini(prompt)
        
        if script is None:
            print("[SCRIPT] ERROR: Could not generate script")
            print("[SCRIPT] Make sure Ollama is running (ollama serve) or GEMINI_API_KEY is set")
            return None
        
        # Save script
        script_path = self.dirs['scripts'] / 'script.txt'
        script_path.write_text(script)
        print(f"[SCRIPT] Saved to: {script_path}")
        
        return script
    
    def _generate_with_ollama(self, prompt):
        """Generate text using local Ollama"""
        try:
            print("[SCRIPT] Using Ollama (local AI)...")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
                timeout=300
            )
            if response.status_code == 200:
                return response.json().get('response', '')
        except Exception as e:
            print(f"[SCRIPT] Ollama not available: {e}")
        return None
    
    def _generate_with_gemini(self, prompt):
        """Generate text using Google Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return None
        
        try:
            print("[SCRIPT] Using Google Gemini API...")
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[SCRIPT] Gemini error: {e}")
        return None
    
    # ==================== VOICE GENERATION ====================
    
    def generate_voiceover(self, script, voice=None):
        """
        Generate voiceover using Edge TTS (100% FREE)
        
        Args:
            script: Text to convert to speech
            voice: Voice ID (default: en-US-GuyNeural)
        """
        print("\n[VOICE] Generating voiceover...")
        
        voice = voice or self.config['voice']
        output_path = self.dirs['voiceovers'] / 'voiceover.mp3'
        
        async def generate():
            import edge_tts
            communicate = edge_tts.Communicate(script, voice)
            await communicate.save(str(output_path))
        
        asyncio.run(generate())
        print(f"[VOICE] Saved to: {output_path}")
        
        return output_path
    
    # ==================== FOOTAGE DOWNLOAD ====================
    
    def download_footage(self, keywords, clips_per_keyword=3):
        """
        Download stock footage from Pexels (FREE API)
        
        Args:
            keywords: List of search keywords
            clips_per_keyword: Number of clips per keyword
        """
        print("\n[FOOTAGE] Downloading stock footage...")
        
        api_key = os.getenv('PEXELS_API_KEY')
        if not api_key:
            print("[FOOTAGE] No PEXELS_API_KEY - creating placeholder")
            return self._create_placeholder_footage()
        
        downloaded = []
        headers = {"Authorization": api_key}
        
        for keyword in keywords:
            print(f"[FOOTAGE] Searching: {keyword}")
            
            try:
                response = requests.get(
                    "https://api.pexels.com/videos/search",
                    headers=headers,
                    params={"query": keyword, "per_page": clips_per_keyword}
                )
                
                if response.status_code != 200:
                    continue
                
                videos = response.json().get('videos', [])
                
                for i, video in enumerate(videos):
                    video_files = video.get('video_files', [])
                    hd_files = [f for f in video_files if f.get('height', 0) >= 720]
                    
                    if not hd_files:
                        continue
                    
                    video_url = hd_files[0].get('link')
                    filename = f"{keyword.replace(' ', '_')}_{i+1}.mp4"
                    output_path = self.dirs['footage'] / filename
                    
                    video_response = requests.get(video_url, stream=True)
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    downloaded.append(output_path)
                    print(f"[FOOTAGE] Downloaded: {filename}")
                    
            except Exception as e:
                print(f"[FOOTAGE] Error: {e}")
        
        if not downloaded:
            return self._create_placeholder_footage()
        
        return downloaded
    
    def _create_placeholder_footage(self):
        """Create placeholder footage if no API key"""
        from moviepy.editor import ColorClip
        
        print("[FOOTAGE] Creating placeholder footage...")
        placeholders = []
        colors = [(30, 60, 90), (60, 30, 90), (90, 60, 30)]
        
        for i, color in enumerate(colors):
            path = self.dirs['footage'] / f'placeholder_{i+1}.mp4'
            clip = ColorClip(
                size=(self.config['width'], self.config['height']),
                color=color,
                duration=30
            )
            clip.write_videofile(str(path), fps=self.config['fps'], 
                               codec='libx264', logger=None)
            clip.close()
            placeholders.append(path)
        
        return placeholders
    
    # ==================== VIDEO ASSEMBLY ====================
    
    def assemble_video(self, voiceover_path, footage_paths):
        """
        Assemble final video from voiceover and footage
        
        Args:
            voiceover_path: Path to voiceover audio
            footage_paths: List of paths to video clips
        """
        print("\n[VIDEO] Assembling video...")
        
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, concatenate_videoclips
        )
        
        # Load audio
        audio = AudioFileClip(str(voiceover_path))
        duration = audio.duration
        print(f"[VIDEO] Audio duration: {duration:.1f} seconds")
        
        # Load and prepare video clips
        clips = []
        total_duration = 0
        
        for path in footage_paths:
            try:
                clip = VideoFileClip(str(path))
                clip = clip.resize((self.config['width'], self.config['height']))
                clips.append(clip)
                total_duration += clip.duration
            except Exception as e:
                print(f"[VIDEO] Could not load {path}: {e}")
        
        if not clips:
            print("[VIDEO] ERROR: No footage available")
            return None
        
        # Loop footage if needed
        if total_duration < duration:
            loops = int(duration / total_duration) + 1
            clips = clips * loops
        
        # Concatenate and trim
        video = concatenate_videoclips(clips)
        video = video.subclip(0, duration)
        
        # Add audio
        video = video.set_audio(audio)
        
        # Export
        output_path = self.dirs['output'] / 'final_video.mp4'
        print(f"[VIDEO] Rendering ({duration:.1f}s)...")
        
        video.write_videofile(
            str(output_path),
            fps=self.config['fps'],
            codec='libx264',
            audio_codec='aac',
            threads=4,
            logger=None
        )
        
        # Cleanup
        audio.close()
        video.close()
        for clip in clips:
            clip.close()
        
        print(f"[VIDEO] Saved to: {output_path}")
        return output_path
    
    # ==================== THUMBNAIL CREATION ====================
    
    def create_thumbnail(self, title, color_scheme='urgent'):
        """
        Create video thumbnail
        
        Args:
            title: Text for thumbnail
            color_scheme: Color scheme (urgent, trust, growth, energy)
        """
        print("\n[THUMBNAIL] Creating thumbnail...")
        
        from PIL import Image, ImageDraw, ImageFont
        
        width, height = 1280, 720
        
        schemes = {
            'urgent': ((220, 53, 69), (180, 30, 50)),
            'trust': ((0, 123, 255), (0, 80, 180)),
            'growth': ((40, 167, 69), (20, 120, 40)),
            'energy': ((255, 193, 7), (220, 160, 0)),
        }
        
        colors = schemes.get(color_scheme, schemes['urgent'])
        
        # Create gradient
        img = Image.new('RGB', (width, height))
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80
            )
        except:
            font = ImageFont.load_default()
        
        # Word wrap
        words = title.upper().split()
        lines = []
        current = []
        
        for word in words:
            current.append(word)
            if len(' '.join(current)) > 15:
                if len(current) > 1:
                    current.pop()
                    lines.append(' '.join(current))
                    current = [word]
        if current:
            lines.append(' '.join(current))
        
        # Draw text
        line_height = 90
        start_y = (height - len(lines) * line_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * line_height
            
            draw.text((x+3, y+3), line, font=font, fill=(0, 0, 0))
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        output_path = self.dirs['thumbnails'] / 'thumbnail.png'
        img.save(str(output_path), quality=95)
        
        print(f"[THUMBNAIL] Saved to: {output_path}")
        return output_path
    
    # ==================== METADATA GENERATION ====================
    
    def generate_metadata(self, topic):
        """Generate video metadata (title, description, tags)"""
        print("\n[METADATA] Generating metadata...")
        
        metadata = {
            'titles': [
                f"{topic} - Complete Guide",
                f"How to Master {topic}",
                f"{topic} Explained Simply",
                f"The Ultimate {topic} Tutorial"
            ],
            'description': f"""In this video, you'll learn everything about {topic}.

We cover all the essential concepts, tips, and strategies you need to succeed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 TIMESTAMPS:
0:00 - Introduction
[Add timestamps after review]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 SUBSCRIBE for more content!

#{"".join(topic.split())} #tutorial #guide
""",
            'tags': [
                topic,
                f"{topic} tutorial",
                f"{topic} guide",
                f"how to {topic}",
                f"{topic} for beginners",
                f"{topic} explained"
            ]
        }
        
        metadata_path = self.dirs['metadata'] / 'metadata.json'
        metadata_path.write_text(json.dumps(metadata, indent=2))
        
        print(f"[METADATA] Saved to: {metadata_path}")
        return metadata
    
    # ==================== MAIN PIPELINE ====================
    
    def run(self, topic, length_minutes=8, footage_keywords=None):
        """
        Run the complete video generation pipeline
        
        Args:
            topic: Video topic
            length_minutes: Target video length
            footage_keywords: Keywords for stock footage search
        """
        print("\n" + "=" * 60)
        print("FACELESS YOUTUBE VIDEO GENERATOR")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Length: {length_minutes} minutes")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Generate script
        script = self.generate_script(topic, length_minutes)
        if not script:
            return None
        
        # Step 2: Generate voiceover
        voiceover = self.generate_voiceover(script)
        
        # Step 3: Download footage
        if footage_keywords is None:
            footage_keywords = topic.split()[:3]
        footage = self.download_footage(footage_keywords)
        
        # Step 4: Assemble video
        video = self.assemble_video(voiceover, footage)
        if not video:
            return None
        
        # Step 5: Create thumbnail
        thumbnail = self.create_thumbnail(topic)
        
        # Step 6: Generate metadata
        metadata = self.generate_metadata(topic)
        
        # Summary
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE!")
        print("=" * 60)
        print(f"Video: {video}")
        print(f"Thumbnail: {thumbnail}")
        print(f"Metadata: {self.dirs['metadata'] / 'metadata.json'}")
        print("=" * 60)
        
        return {
            'video': str(video),
            'thumbnail': str(thumbnail),
            'metadata': metadata,
            'project_dir': str(self.base_dir)
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate faceless YouTube videos automatically'
    )
    parser.add_argument(
        '--topic', '-t',
        required=True,
        help='Video topic'
    )
    parser.add_argument(
        '--length', '-l',
        type=int,
        default=8,
        help='Video length in minutes (default: 8)'
    )
    parser.add_argument(
        '--keywords', '-k',
        nargs='+',
        help='Keywords for stock footage search'
    )
    parser.add_argument(
        '--project', '-p',
        help='Project name (default: auto-generated)'
    )
    
    args = parser.parse_args()
    
    generator = FacelessVideoGenerator(project_name=args.project)
    result = generator.run(
        topic=args.topic,
        length_minutes=args.length,
        footage_keywords=args.keywords
    )
    
    if result:
        print("\nYour video is ready!")
        print(f"Project directory: {result['project_dir']}")
        return 0
    else:
        print("\nVideo generation failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
