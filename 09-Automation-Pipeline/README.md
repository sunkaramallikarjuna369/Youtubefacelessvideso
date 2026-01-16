# Module 9: Complete Automation Pipeline

## Overview

This module brings everything together into a complete automation pipeline. You'll learn how to automate the entire video creation process from script to final video with minimal manual intervention.

## The Complete Pipeline

```
1. Topic Research → 2. Script Generation → 3. Voice Generation → 
4. Footage Download → 5. Video Assembly → 6. Thumbnail Creation → 
7. Metadata Generation → 8. Upload to YouTube
```

## Project Structure

```
my_video_project/
├── config.json           # Project configuration
├── scripts/              # Generated scripts
├── voiceovers/           # Generated audio files
├── footage/              # Downloaded stock footage
├── thumbnails/           # Generated thumbnails
├── output/               # Final videos
└── metadata/             # Titles, descriptions, tags
```

## Complete Automation Script

```python
#!/usr/bin/env python3
"""
COMPLETE VIDEO AUTOMATION PIPELINE
Generates faceless YouTube videos from topic to final video

Requirements:
pip install edge-tts moviepy Pillow requests python-dotenv
"""

import os
import json
import asyncio
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VideoAutomationPipeline:
    """Complete pipeline for automated video creation"""
    
    def __init__(self, project_name, output_dir="projects"):
        self.project_name = project_name
        self.project_dir = os.path.join(output_dir, project_name)
        
        # Create directory structure
        self.dirs = {
            'scripts': os.path.join(self.project_dir, 'scripts'),
            'voiceovers': os.path.join(self.project_dir, 'voiceovers'),
            'footage': os.path.join(self.project_dir, 'footage'),
            'thumbnails': os.path.join(self.project_dir, 'thumbnails'),
            'output': os.path.join(self.project_dir, 'output'),
            'metadata': os.path.join(self.project_dir, 'metadata')
        }
        
        for d in self.dirs.values():
            os.makedirs(d, exist_ok=True)
        
        # Configuration
        self.config = {
            'voice': 'en-US-GuyNeural',
            'video_width': 1920,
            'video_height': 1080,
            'fps': 30
        }
        
        print(f"Project initialized: {self.project_dir}")
    
    # ==================== STEP 1: SCRIPT GENERATION ====================
    
    def generate_script_with_ollama(self, topic, video_length_minutes=8):
        """Generate script using local Ollama (FREE)"""
        print(f"\n[STEP 1] Generating script for: {topic}")
        
        word_count = video_length_minutes * 150
        
        prompt = f"""Write a YouTube video script about: {topic}

Requirements:
- Approximately {word_count} words ({video_length_minutes} minutes when spoken)
- Start with an attention-grabbing hook (first 30 seconds)
- Include 4-5 main sections with clear transitions
- Add [SECTION: Title] markers before each section
- Add [VISUAL: description] markers for B-roll suggestions
- End with a strong call to action
- Conversational, engaging tone
- No stage directions or narrator notes

Write the complete script now:"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300
            )
            
            script = response.json().get('response', '')
            
            # Save script
            script_path = os.path.join(self.dirs['scripts'], 'full_script.txt')
            with open(script_path, 'w') as f:
                f.write(script)
            
            print(f"Script saved: {script_path}")
            return script
            
        except requests.exceptions.ConnectionError:
            print("ERROR: Ollama not running. Start with: ollama serve")
            return None
    
    def generate_script_with_gemini(self, topic, video_length_minutes=8):
        """Generate script using Google Gemini (FREE tier)"""
        print(f"\n[STEP 1] Generating script with Gemini for: {topic}")
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("ERROR: GEMINI_API_KEY not set in .env file")
            return None
        
        word_count = video_length_minutes * 150
        
        prompt = f"""Write a YouTube video script about: {topic}

Requirements:
- Approximately {word_count} words ({video_length_minutes} minutes when spoken)
- Start with an attention-grabbing hook
- Include 4-5 main sections
- Add [SECTION: Title] markers before each section
- Add [VISUAL: description] markers for B-roll
- End with call to action
- Conversational tone

Write the complete script:"""

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            script = response.text
            
            script_path = os.path.join(self.dirs['scripts'], 'full_script.txt')
            with open(script_path, 'w') as f:
                f.write(script)
            
            print(f"Script saved: {script_path}")
            return script
            
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    # ==================== STEP 2: VOICE GENERATION ====================
    
    async def _generate_voice_async(self, text, output_file, voice):
        """Async voice generation"""
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    
    def generate_voiceover(self, script, voice=None):
        """Generate voiceover using Edge TTS (FREE)"""
        print("\n[STEP 2] Generating voiceover...")
        
        voice = voice or self.config['voice']
        output_file = os.path.join(self.dirs['voiceovers'], 'voiceover.mp3')
        
        # Clean script for TTS (remove markers)
        clean_script = script
        for marker in ['[SECTION:', '[VISUAL:', '[']:
            while marker in clean_script:
                start = clean_script.find(marker)
                end = clean_script.find(']', start) + 1
                if end > start:
                    clean_script = clean_script[:start] + clean_script[end:]
                else:
                    break
        
        asyncio.run(self._generate_voice_async(clean_script, output_file, voice))
        
        print(f"Voiceover saved: {output_file}")
        return output_file
    
    # ==================== STEP 3: FOOTAGE DOWNLOAD ====================
    
    def download_stock_footage(self, keywords, clips_per_keyword=3):
        """Download stock footage from Pexels (FREE)"""
        print("\n[STEP 3] Downloading stock footage...")
        
        api_key = os.getenv('PEXELS_API_KEY')
        if not api_key:
            print("WARNING: PEXELS_API_KEY not set. Using placeholder footage.")
            return self._create_placeholder_footage()
        
        headers = {"Authorization": api_key}
        downloaded = []
        
        for keyword in keywords:
            print(f"  Searching: {keyword}")
            
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
                
                # Get HD quality
                hd_files = [f for f in video_files if f.get('height', 0) >= 720]
                if not hd_files:
                    continue
                
                video_url = hd_files[0].get('link')
                filename = f"{keyword.replace(' ', '_')}_{i+1}.mp4"
                output_path = os.path.join(self.dirs['footage'], filename)
                
                # Download
                video_response = requests.get(video_url, stream=True)
                with open(output_path, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                downloaded.append(output_path)
                print(f"    Downloaded: {filename}")
        
        print(f"Total footage downloaded: {len(downloaded)} clips")
        return downloaded
    
    def _create_placeholder_footage(self):
        """Create placeholder footage if no API key"""
        from moviepy.editor import ColorClip
        
        colors = [(30, 60, 90), (60, 90, 30), (90, 30, 60)]
        placeholders = []
        
        for i, color in enumerate(colors):
            clip = ColorClip(
                size=(self.config['video_width'], self.config['video_height']),
                color=color,
                duration=30
            )
            path = os.path.join(self.dirs['footage'], f'placeholder_{i+1}.mp4')
            clip.write_videofile(path, fps=self.config['fps'], codec='libx264')
            placeholders.append(path)
            clip.close()
        
        return placeholders
    
    # ==================== STEP 4: VIDEO ASSEMBLY ====================
    
    def assemble_video(self, voiceover_path, footage_paths):
        """Assemble final video"""
        print("\n[STEP 4] Assembling video...")
        
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, concatenate_videoclips,
            CompositeVideoClip, ColorClip
        )
        
        # Load audio
        audio = AudioFileClip(voiceover_path)
        audio_duration = audio.duration
        
        # Load and prepare video clips
        video_clips = []
        total_video_duration = 0
        
        for footage_path in footage_paths:
            try:
                clip = VideoFileClip(footage_path)
                clip = clip.resize((self.config['video_width'], self.config['video_height']))
                video_clips.append(clip)
                total_video_duration += clip.duration
            except Exception as e:
                print(f"  Warning: Could not load {footage_path}: {e}")
        
        if not video_clips:
            print("  No footage available, creating color background")
            bg = ColorClip(
                size=(self.config['video_width'], self.config['video_height']),
                color=(30, 30, 50),
                duration=audio_duration
            )
            video_clips = [bg]
            total_video_duration = audio_duration
        
        # Loop footage if needed
        if total_video_duration < audio_duration:
            loops_needed = int(audio_duration / total_video_duration) + 1
            video_clips = video_clips * loops_needed
        
        # Concatenate and trim
        final_video = concatenate_videoclips(video_clips)
        final_video = final_video.subclip(0, audio_duration)
        
        # Add audio
        final_video = final_video.set_audio(audio)
        
        # Export
        output_path = os.path.join(self.dirs['output'], 'final_video.mp4')
        
        print(f"  Rendering video ({audio_duration:.1f} seconds)...")
        final_video.write_videofile(
            output_path,
            fps=self.config['fps'],
            codec='libx264',
            audio_codec='aac',
            threads=4
        )
        
        # Cleanup
        audio.close()
        final_video.close()
        for clip in video_clips:
            clip.close()
        
        print(f"Video saved: {output_path}")
        return output_path
    
    # ==================== STEP 5: THUMBNAIL CREATION ====================
    
    def create_thumbnail(self, title, color_scheme='urgent'):
        """Create video thumbnail"""
        print("\n[STEP 5] Creating thumbnail...")
        
        from PIL import Image, ImageDraw, ImageFont
        
        width, height = 1280, 720
        
        # Color schemes
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
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Add text
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
            
            # Shadow
            draw.text((x+3, y+3), line, font=font, fill=(0, 0, 0))
            # Main text
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        output_path = os.path.join(self.dirs['thumbnails'], 'thumbnail.png')
        img.save(output_path, quality=95)
        
        print(f"Thumbnail saved: {output_path}")
        return output_path
    
    # ==================== STEP 6: METADATA GENERATION ====================
    
    def generate_metadata(self, topic, script):
        """Generate title, description, and tags"""
        print("\n[STEP 6] Generating metadata...")
        
        # Generate title variations
        titles = [
            f"{topic} - Complete Guide",
            f"How to Master {topic} (Step by Step)",
            f"{topic} Explained Simply",
            f"The Ultimate {topic} Tutorial"
        ]
        
        # Generate description
        description = f"""In this video, you'll learn everything about {topic}.

We cover all the essential concepts, tips, and strategies you need to succeed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 TIMESTAMPS:
0:00 - Introduction
[Add more timestamps after review]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 SUBSCRIBE for more content like this!

#{"".join(topic.split())} #tutorial #guide
"""
        
        # Generate tags
        words = topic.lower().split()
        tags = [
            topic,
            f"{topic} tutorial",
            f"{topic} guide",
            f"how to {topic}",
            f"{topic} for beginners",
            f"{topic} explained",
            f"{topic} tips",
        ]
        tags.extend(words)
        
        metadata = {
            'titles': titles,
            'description': description,
            'tags': tags[:20]
        }
        
        # Save metadata
        metadata_path = os.path.join(self.dirs['metadata'], 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Metadata saved: {metadata_path}")
        return metadata
    
    # ==================== MAIN PIPELINE ====================
    
    def run_full_pipeline(self, topic, footage_keywords=None, 
                         use_gemini=False, video_length=8):
        """Run the complete video creation pipeline"""
        print("=" * 60)
        print("FACELESS YOUTUBE VIDEO AUTOMATION PIPELINE")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Generate Script
        if use_gemini:
            script = self.generate_script_with_gemini(topic, video_length)
        else:
            script = self.generate_script_with_ollama(topic, video_length)
        
        if not script:
            print("ERROR: Script generation failed")
            return None
        
        # Step 2: Generate Voiceover
        voiceover = self.generate_voiceover(script)
        
        # Step 3: Download Footage
        if footage_keywords is None:
            footage_keywords = topic.split()[:3]
        footage = self.download_stock_footage(footage_keywords)
        
        # Step 4: Assemble Video
        video = self.assemble_video(voiceover, footage)
        
        # Step 5: Create Thumbnail
        thumbnail = self.create_thumbnail(topic)
        
        # Step 6: Generate Metadata
        metadata = self.generate_metadata(topic, script)
        
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE!")
        print("=" * 60)
        print(f"Video: {video}")
        print(f"Thumbnail: {thumbnail}")
        print(f"Metadata: {self.dirs['metadata']}/metadata.json")
        print("=" * 60)
        
        return {
            'video': video,
            'thumbnail': thumbnail,
            'metadata': metadata,
            'script': script
        }


# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Create pipeline
    pipeline = VideoAutomationPipeline(
        project_name="my_first_video"
    )
    
    # Run full pipeline
    result = pipeline.run_full_pipeline(
        topic="5 AI Tools That Will Change Your Life",
        footage_keywords=["artificial intelligence", "technology", "productivity"],
        use_gemini=False,  # Set to True to use Gemini instead of Ollama
        video_length=8  # minutes
    )
    
    if result:
        print("\nYour video is ready!")
        print(f"Video file: {result['video']}")
        print(f"Thumbnail: {result['thumbnail']}")
        print("\nNext steps:")
        print("1. Review the video")
        print("2. Upload to YouTube")
        print("3. Use the generated metadata")
```

## Quick Start Guide

### 1. Install Requirements

```bash
pip install edge-tts moviepy Pillow requests python-dotenv
```

### 2. Set Up Environment

Create a `.env` file:
```
PEXELS_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here  # Optional
```

### 3. Start Ollama (if using local AI)

```bash
ollama serve
```

### 4. Run the Pipeline

```python
from automation_pipeline import VideoAutomationPipeline

pipeline = VideoAutomationPipeline("my_video")
result = pipeline.run_full_pipeline(
    topic="Your Video Topic Here",
    footage_keywords=["keyword1", "keyword2"],
    video_length=8
)
```

## Batch Video Generation

```python
#!/usr/bin/env python3
"""
Batch Video Generator
Create multiple videos automatically
"""

from automation_pipeline import VideoAutomationPipeline
import time

def batch_generate(topics):
    """Generate multiple videos"""
    results = []
    
    for i, topic_config in enumerate(topics):
        print(f"\n{'='*60}")
        print(f"GENERATING VIDEO {i+1}/{len(topics)}")
        print(f"{'='*60}")
        
        topic = topic_config['topic']
        keywords = topic_config.get('keywords', topic.split()[:3])
        
        # Create unique project name
        project_name = f"video_{i+1}_{int(time.time())}"
        
        pipeline = VideoAutomationPipeline(project_name)
        result = pipeline.run_full_pipeline(
            topic=topic,
            footage_keywords=keywords,
            video_length=topic_config.get('length', 8)
        )
        
        if result:
            results.append({
                'topic': topic,
                'project': project_name,
                'video': result['video']
            })
        
        # Wait between videos to avoid rate limits
        time.sleep(5)
    
    return results


if __name__ == "__main__":
    # Define videos to create
    topics = [
        {
            'topic': '5 Morning Habits for Success',
            'keywords': ['morning routine', 'productivity', 'success'],
            'length': 8
        },
        {
            'topic': 'How to Learn Any Skill Fast',
            'keywords': ['learning', 'education', 'skills'],
            'length': 10
        },
        {
            'topic': 'Money Management Tips for Beginners',
            'keywords': ['finance', 'money', 'budgeting'],
            'length': 8
        }
    ]
    
    results = batch_generate(topics)
    
    print("\n" + "="*60)
    print("BATCH GENERATION COMPLETE")
    print("="*60)
    for r in results:
        print(f"  {r['topic']}: {r['video']}")
```

## Scheduling Videos

```python
#!/usr/bin/env python3
"""
Video Scheduler
Schedule video generation for specific times
"""

import schedule
import time
from automation_pipeline import VideoAutomationPipeline

def create_scheduled_video():
    """Create a video on schedule"""
    topics = [
        "Productivity Tips for Remote Workers",
        "Best Free Apps for Students",
        "How to Stay Motivated Every Day"
    ]
    
    import random
    topic = random.choice(topics)
    
    pipeline = VideoAutomationPipeline(f"scheduled_{int(time.time())}")
    pipeline.run_full_pipeline(topic=topic)

# Schedule videos
schedule.every().monday.at("09:00").do(create_scheduled_video)
schedule.every().thursday.at("09:00").do(create_scheduled_video)

print("Scheduler running... Press Ctrl+C to stop")
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Pipeline Checklist

Before running the pipeline:

- [ ] Python 3.8+ installed
- [ ] All packages installed (edge-tts, moviepy, Pillow, requests)
- [ ] Ollama installed and running (or Gemini API key set)
- [ ] Pexels API key set (optional but recommended)
- [ ] Sufficient disk space for videos

## Troubleshooting

**"Ollama connection refused"**
- Start Ollama: `ollama serve`

**"No footage downloaded"**
- Check PEXELS_API_KEY in .env file
- Pipeline will create placeholder footage if no API key

**"MoviePy error"**
- Install FFmpeg: `sudo apt install ffmpeg` (Linux) or download from ffmpeg.org

**"Out of memory"**
- Reduce video length
- Close other applications
- Process fewer footage clips

## Next Steps

1. Run your first automated video
2. Review and adjust the output
3. Move to Module 10 for YouTube upload automation

---

## Additional Resources

- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [Edge TTS GitHub](https://github.com/rany2/edge-tts)
- [Pexels API](https://www.pexels.com/api/)
