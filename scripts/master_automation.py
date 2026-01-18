#!/usr/bin/env python3
"""
MASTER AUTOMATION SCRIPT
Complete Faceless YouTube Video Generation Pipeline

This script automates the entire process from topic to uploaded video:
1. Suggest trending topics (with monetization focus)
2. Generate video topic ideas
3. Write script with AI (Gemini, Groq, or Ollama)
4. Generate voiceover
5. Download stock footage (Pexels + Pixabay)
6. Assemble video
7. Create thumbnail
8. Generate metadata
9. Upload to YouTube (optional)

Requirements:
pip install edge-tts moviepy Pillow requests python-dotenv google-generativeai groq pytrends

Usage:
python master_automation.py --topic "Your Video Topic" --length 8
python master_automation.py --suggest-topics  # Get trending topic suggestions
python master_automation.py --interactive     # Interactive mode with prompts

Author: Faceless YouTube Automation Course
"""

import os
import sys
import json
import asyncio
import argparse
import requests
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_trending_topics(niche=None):
    """
    Get trending topics from Google Trends with monetization focus.
    High CPM niches: Finance, Tech, Health, Education, Business, Legal
    """
    print("\n" + "=" * 60)
    print("TRENDING TOPIC SUGGESTIONS (Monetization Focused)")
    print("=" * 60)
    
    # High CPM niches for better monetization
    high_cpm_niches = {
        'finance': {
            'keywords': ['investing', 'stocks', 'crypto', 'money', 'budget', 'savings', 'wealth'],
            'cpm_range': '$15-$50',
            'topics': [
                "5 Investment Mistakes That Cost You Thousands",
                "How to Build Wealth in Your 20s",
                "Passive Income Ideas That Actually Work",
                "Stock Market Secrets for Beginners",
                "Crypto Investing Guide for 2024"
            ]
        },
        'technology': {
            'keywords': ['AI', 'software', 'gadgets', 'apps', 'coding', 'tech'],
            'cpm_range': '$10-$30',
            'topics': [
                "AI Tools That Will Change Your Life",
                "Best Productivity Apps You Need",
                "Future Technology That Will Blow Your Mind",
                "Coding Tips Every Developer Should Know",
                "Tech Gadgets Worth Your Money"
            ]
        },
        'health': {
            'keywords': ['fitness', 'nutrition', 'wellness', 'diet', 'exercise', 'mental health'],
            'cpm_range': '$10-$25',
            'topics': [
                "Morning Habits of Successful People",
                "Foods That Boost Your Brain Power",
                "Simple Exercises for Better Health",
                "Mental Health Tips Everyone Needs",
                "Sleep Hacks for Better Rest"
            ]
        },
        'education': {
            'keywords': ['learning', 'study', 'skills', 'career', 'courses', 'knowledge'],
            'cpm_range': '$8-$20',
            'topics': [
                "Skills That Will Make You Rich",
                "How to Learn Anything Fast",
                "Career Advice Nobody Tells You",
                "Study Techniques That Actually Work",
                "Online Courses Worth Taking"
            ]
        },
        'business': {
            'keywords': ['entrepreneur', 'startup', 'marketing', 'sales', 'business'],
            'cpm_range': '$12-$35',
            'topics': [
                "Business Ideas You Can Start Today",
                "Marketing Strategies That Work",
                "How to Start a Side Hustle",
                "Entrepreneur Mistakes to Avoid",
                "Passive Income Business Ideas"
            ]
        }
    }
    
    # Try to get real-time trends from Google
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl='en-US', tz=360)
        trending = pytrends.trending_searches(pn='united_states')
        real_trends = trending[0].tolist()[:10]
        print("\nReal-time Google Trends:")
        for i, trend in enumerate(real_trends, 1):
            print(f"  {i}. {trend}")
    except Exception as e:
        print(f"\nCould not fetch real-time trends: {e}")
        real_trends = []
    
    print("\n" + "-" * 60)
    print("HIGH CPM TOPIC SUGGESTIONS (Better Monetization):")
    print("-" * 60)
    
    suggestions = []
    for niche_name, niche_data in high_cpm_niches.items():
        print(f"\n[{niche_name.upper()}] - CPM: {niche_data['cpm_range']}")
        for topic in niche_data['topics'][:3]:
            print(f"  - {topic}")
            suggestions.append({'niche': niche_name, 'topic': topic, 'cpm': niche_data['cpm_range']})
    
    print("\n" + "=" * 60)
    print("TIP: Finance and Business topics typically have the highest CPM!")
    print("=" * 60)
    
    return suggestions


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
    
    def generate_script(self, topic, length_minutes=8, ai_provider='auto'):
        """
        Generate a video script using AI
        
        Args:
            topic: Video topic
            length_minutes: Target video length
            ai_provider: 'auto', 'groq', 'gemini', or 'ollama'
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
- Make it informative and valuable for viewers

Write the complete script now:"""

        script = None
        
        # Try AI providers in order of preference
        if ai_provider == 'auto':
            # Try Groq first (fastest), then Gemini, then Ollama
            script = self._generate_with_groq(prompt)
            if script is None:
                script = self._generate_with_gemini(prompt)
            if script is None:
                script = self._generate_with_ollama(prompt)
        elif ai_provider == 'groq':
            script = self._generate_with_groq(prompt)
        elif ai_provider == 'gemini':
            script = self._generate_with_gemini(prompt)
        elif ai_provider == 'ollama':
            script = self._generate_with_ollama(prompt)
        
        if script is None:
            print("[SCRIPT] ERROR: Could not generate script")
            print("[SCRIPT] Make sure you have set API keys in .env file:")
            print("  - GROQ_API_KEY (fastest)")
            print("  - GEMINI_API_KEY")
            print("  - Or run Ollama locally (ollama serve)")
            return None
        
        # Save script
        script_path = self.dirs['scripts'] / 'script.txt'
        script_path.write_text(script)
        print(f"[SCRIPT] Saved to: {script_path}")
        
        return script
    
    def _generate_with_groq(self, prompt):
        """Generate text using Groq API (fastest)"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("[SCRIPT] No GROQ_API_KEY found")
            return None
        
        try:
            print("[SCRIPT] Using Groq API (fastest)...")
            from groq import Groq
            client = Groq(api_key=api_key)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a professional YouTube script writer who creates engaging, informative content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[SCRIPT] Groq error: {e}")
        return None
    
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
            print("[SCRIPT] No GEMINI_API_KEY found")
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
    
    # ==================== SEGMENT-BASED KEYWORD EXTRACTION ====================
    
    def extract_segment_keywords(self, script, ai_provider='auto'):
        """
        Extract keywords for each section of the script for better footage matching.
        This enables segment-based footage that matches what's being said.
        
        Args:
            script: The full video script
            ai_provider: AI provider to use for extraction
            
        Returns:
            List of dicts with 'text' and 'keywords' for each segment
        """
        print("\n[KEYWORDS] Extracting segment-based keywords for better footage matching...")
        
        prompt = f"""Analyze this video script and divide it into 5-7 logical sections.
For each section, provide 2-3 specific keywords that would find relevant stock footage.

Script:
{script[:3000]}

Return ONLY a JSON array in this exact format (no other text):
[
  {{"section": 1, "summary": "brief description", "keywords": ["keyword1", "keyword2"]}},
  {{"section": 2, "summary": "brief description", "keywords": ["keyword1", "keyword2"]}}
]

Make keywords specific and visual (e.g., "person typing laptop" not "productivity").
Focus on scenes that can be found in stock footage libraries."""

        result = None
        
        if ai_provider == 'auto':
            result = self._generate_with_groq(prompt)
            if result is None:
                result = self._generate_with_gemini(prompt)
        elif ai_provider == 'groq':
            result = self._generate_with_groq(prompt)
        elif ai_provider == 'gemini':
            result = self._generate_with_gemini(prompt)
        
        if result is None:
            print("[KEYWORDS] Could not extract keywords, using topic-based fallback")
            return None
        
        try:
            import re
            json_match = re.search(r'\[[\s\S]*\]', result)
            if json_match:
                segments = json.loads(json_match.group())
                print(f"[KEYWORDS] Extracted {len(segments)} segments:")
                for seg in segments:
                    print(f"  Section {seg.get('section', '?')}: {seg.get('keywords', [])}")
                return segments
        except Exception as e:
            print(f"[KEYWORDS] Error parsing keywords: {e}")
        
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
        Download stock footage from Pexels and Pixabay (FREE APIs)
        
        Args:
            keywords: List of search keywords
            clips_per_keyword: Number of clips per keyword
        """
        print("\n[FOOTAGE] Downloading stock footage...")
        
        downloaded = []
        
        # Try Pexels first
        pexels_clips = self._download_from_pexels(keywords, clips_per_keyword)
        downloaded.extend(pexels_clips)
        
        # If not enough clips, try Pixabay
        if len(downloaded) < clips_per_keyword * len(keywords):
            pixabay_clips = self._download_from_pixabay(keywords, clips_per_keyword)
            downloaded.extend(pixabay_clips)
        
        if not downloaded:
            print("[FOOTAGE] No clips downloaded, creating placeholders...")
            return self._create_placeholder_footage()
        
        print(f"[FOOTAGE] Total clips downloaded: {len(downloaded)}")
        return downloaded
    
    def download_segment_footage(self, segments, clips_per_segment=2):
        """
        Download footage for each script segment for better matching.
        
        Args:
            segments: List of segment dicts with 'keywords' field
            clips_per_segment: Number of clips per segment
            
        Returns:
            List of lists, where each inner list contains footage paths for that segment
        """
        print("\n[FOOTAGE] Downloading segment-based footage for better matching...")
        
        segment_footage = []
        
        for i, segment in enumerate(segments):
            keywords = segment.get('keywords', [])
            if not keywords:
                continue
                
            print(f"\n[FOOTAGE] Segment {i+1}: {keywords}")
            
            segment_clips = []
            
            # Try Pexels first
            for keyword in keywords[:2]:
                pexels_clips = self._download_from_pexels([keyword], clips_per_segment)
                segment_clips.extend(pexels_clips)
                if len(segment_clips) >= clips_per_segment:
                    break
            
            # If not enough, try Pixabay
            if len(segment_clips) < clips_per_segment:
                for keyword in keywords[:2]:
                    pixabay_clips = self._download_from_pixabay([keyword], clips_per_segment)
                    segment_clips.extend(pixabay_clips)
                    if len(segment_clips) >= clips_per_segment:
                        break
            
            segment_footage.append(segment_clips)
            print(f"[FOOTAGE] Segment {i+1}: {len(segment_clips)} clips downloaded")
        
        total_clips = sum(len(clips) for clips in segment_footage)
        print(f"\n[FOOTAGE] Total clips downloaded: {total_clips} across {len(segment_footage)} segments")
        
        return segment_footage
    
    def _download_from_pexels(self, keywords, clips_per_keyword):
        """Download footage from Pexels API"""
        api_key = os.getenv('PEXELS_API_KEY')
        if not api_key:
            print("[FOOTAGE] No PEXELS_API_KEY - skipping Pexels")
            return []
        
        downloaded = []
        headers = {"Authorization": api_key}
        
        for keyword in keywords:
            print(f"[FOOTAGE] Searching Pexels: {keyword}")
            
            try:
                response = requests.get(
                    "https://api.pexels.com/videos/search",
                    headers=headers,
                    params={"query": keyword, "per_page": clips_per_keyword}
                )
                
                if response.status_code != 200:
                    print(f"[FOOTAGE] Pexels API error: {response.status_code}")
                    continue
                
                videos = response.json().get('videos', [])
                
                for i, video in enumerate(videos):
                    video_files = video.get('video_files', [])
                    hd_files = [f for f in video_files if f.get('height', 0) >= 720]
                    
                    if not hd_files:
                        continue
                    
                    video_url = hd_files[0].get('link')
                    filename = f"pexels_{keyword.replace(' ', '_')}_{i+1}.mp4"
                    output_path = self.dirs['footage'] / filename
                    
                    video_response = requests.get(video_url, stream=True)
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    downloaded.append(output_path)
                    print(f"[FOOTAGE] Downloaded: {filename}")
                    
            except Exception as e:
                print(f"[FOOTAGE] Pexels error: {e}")
        
        return downloaded
    
    def _download_from_pixabay(self, keywords, clips_per_keyword):
        """Download footage from Pixabay API"""
        api_key = os.getenv('PIXABAY_API_KEY')
        if not api_key:
            print("[FOOTAGE] No PIXABAY_API_KEY - skipping Pixabay")
            return []
        
        downloaded = []
        
        for keyword in keywords:
            print(f"[FOOTAGE] Searching Pixabay: {keyword}")
            
            try:
                response = requests.get(
                    "https://pixabay.com/api/videos/",
                    params={
                        "key": api_key,
                        "q": keyword,
                        "per_page": clips_per_keyword,
                        "video_type": "film"
                    }
                )
                
                if response.status_code != 200:
                    print(f"[FOOTAGE] Pixabay API error: {response.status_code}")
                    continue
                
                videos = response.json().get('hits', [])
                
                for i, video in enumerate(videos):
                    # Get medium quality video (good balance of quality and size)
                    video_url = video.get('videos', {}).get('medium', {}).get('url')
                    if not video_url:
                        video_url = video.get('videos', {}).get('small', {}).get('url')
                    
                    if not video_url:
                        continue
                    
                    filename = f"pixabay_{keyword.replace(' ', '_')}_{i+1}.mp4"
                    output_path = self.dirs['footage'] / filename
                    
                    video_response = requests.get(video_url, stream=True)
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    downloaded.append(output_path)
                    print(f"[FOOTAGE] Downloaded: {filename}")
                    
            except Exception as e:
                print(f"[FOOTAGE] Pixabay error: {e}")
        
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
    
    def extract_key_points(self, script, ai_provider='auto'):
        """
        Extract key points from script for text overlays.
        
        Args:
            script: The video script
            ai_provider: AI provider to use
            
        Returns:
            List of key point strings to display on screen
        """
        print("[VIDEO] Extracting key points for text overlays...")
        
        prompt = f"""Extract 8-12 key points from this video script that should be displayed as text overlays.
Each point should be:
- Short (3-7 words max)
- A key fact, tip, or important statement
- Easy to read quickly on screen

Script:
{script[:3000]}

Return ONLY a JSON array of strings, no other text:
["Key point 1", "Key point 2", "Key point 3"]"""

        result = None
        
        if ai_provider == 'auto':
            result = self._generate_with_groq(prompt)
            if result is None:
                result = self._generate_with_gemini(prompt)
        elif ai_provider == 'groq':
            result = self._generate_with_groq(prompt)
        elif ai_provider == 'gemini':
            result = self._generate_with_gemini(prompt)
        
        if result:
            try:
                import re
                json_match = re.search(r'\[[\s\S]*?\]', result)
                if json_match:
                    key_points = json.loads(json_match.group())
                    print(f"[VIDEO] Extracted {len(key_points)} key points for overlays")
                    return key_points
            except Exception as e:
                print(f"[VIDEO] Error parsing key points: {e}")
        
        return None
    
    def create_text_image(self, text, width, height):
        """
        Create a text overlay image using PIL (no ImageMagick required).
        
        Args:
            text: Text to display
            width: Image width
            height: Image height
            
        Returns:
            Path to the created image
        """
        from PIL import Image, ImageDraw, ImageFont
        import tempfile
        
        # Create transparent image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fall back to default
        font_size = 50
        try:
            # Try common Windows fonts first
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/arialbd.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]
            font = None
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Word wrap text
        words = text.upper().split()
        lines = []
        current_line = []
        max_width = width - 100
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate text position (bottom third of screen)
        line_height = font_size + 10
        total_text_height = len(lines) * line_height
        y_start = int(height * 0.75) - total_text_height // 2
        
        # Draw text with outline
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = y_start + i * line_height
            
            # Draw black outline
            outline_width = 3
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0, 255))
            
            # Draw white text
            draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        
        # Save to temp file
        temp_path = tempfile.mktemp(suffix='.png')
        img.save(temp_path, 'PNG')
        
        return temp_path
    
    def assemble_video(self, voiceover_path, footage_paths, script=None, ai_provider='auto'):
        """
        Assemble final video from voiceover and footage with text overlays
        
        Args:
            voiceover_path: Path to voiceover audio
            footage_paths: List of paths to video clips
            script: Optional script for extracting key points for text overlays
            ai_provider: AI provider for key point extraction
        """
        print("\n[VIDEO] Assembling video...")
        
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, concatenate_videoclips,
            ImageClip, CompositeVideoClip
        )
        
        # Load audio
        audio = AudioFileClip(str(voiceover_path))
        duration = audio.duration
        print(f"[VIDEO] Audio duration: {duration:.1f} seconds")
        
        # Extract key points for text overlays if script provided
        key_points = None
        if script:
            key_points = self.extract_key_points(script, ai_provider)
        
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
        
        # Add text overlays if key points available (using PIL, no ImageMagick needed)
        text_image_paths = []
        if key_points and len(key_points) > 0:
            print(f"[VIDEO] Adding {len(key_points)} text overlays (using PIL)...")
            
            try:
                # Calculate timing for each key point
                interval = duration / (len(key_points) + 1)
                text_clips = []
                
                for i, point in enumerate(key_points):
                    start_time = (i + 1) * interval - 2.5  # Start 2.5 seconds before center
                    if start_time < 0:
                        start_time = 0
                    
                    try:
                        # Create text image using PIL
                        text_img_path = self.create_text_image(
                            point, 
                            self.config['width'], 
                            self.config['height']
                        )
                        text_image_paths.append(text_img_path)
                        
                        # Create ImageClip with transparency support
                        txt_clip = ImageClip(text_img_path, transparent=True)
                        txt_clip = txt_clip.set_start(start_time)
                        txt_clip = txt_clip.set_duration(5)  # Show for 5 seconds
                        
                        text_clips.append(txt_clip)
                        print(f"[VIDEO] Created overlay {i+1}/{len(key_points)}: {point[:30]}...")
                    except Exception as e:
                        print(f"[VIDEO] Could not create text overlay {i+1}: {e}")
                
                if text_clips:
                    # Composite video with text overlays
                    print(f"[VIDEO] Compositing {len(text_clips)} text overlays with video...")
                    video = CompositeVideoClip([video] + text_clips, size=(self.config['width'], self.config['height']))
                    print(f"[VIDEO] Successfully added {len(text_clips)} text overlays")
            except Exception as e:
                print(f"[VIDEO] Error adding text overlays, continuing without them: {e}")
                import traceback
                traceback.print_exc()
        
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
            try:
                clip.close()
            except:
                pass
        
        # Clean up temp text images
        import os
        for img_path in text_image_paths:
            try:
                os.remove(img_path)
            except:
                pass
        
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
    
    def run(self, topic, length_minutes=8, footage_keywords=None, ai_provider='auto'):
        """
        Run the complete video generation pipeline
        
        Args:
            topic: Video topic
            length_minutes: Target video length (default: 8 minutes)
            footage_keywords: Keywords for stock footage search (if None, uses AI-based segment extraction)
            ai_provider: AI provider for script generation ('auto', 'groq', 'gemini', 'ollama')
        """
        print("\n" + "=" * 60)
        print("FACELESS YOUTUBE VIDEO GENERATOR")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Length: {length_minutes} minutes")
        print(f"AI Provider: {ai_provider}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Step 1: Generate script
        script = self.generate_script(topic, length_minutes, ai_provider)
        if not script:
            return None
        
        # Step 2: Generate voiceover
        voiceover = self.generate_voiceover(script)
        
        # Step 3: Download footage with smart segment-based matching
        if footage_keywords is None:
            # Try AI-based segment extraction for better footage matching
            segments = self.extract_segment_keywords(script, ai_provider)
            
            if segments and len(segments) > 0:
                # Use segment-based footage for better relevance
                segment_footage = self.download_segment_footage(segments, clips_per_segment=2)
                # Flatten the segment footage into a single list
                footage = []
                for seg_clips in segment_footage:
                    footage.extend(seg_clips)
                
                if not footage:
                    # Fallback to topic-based keywords
                    print("[FOOTAGE] Segment-based download failed, using topic keywords...")
                    footage_keywords = topic.split()[:3]
                    footage = self.download_footage(footage_keywords)
            else:
                # Fallback to topic-based keywords
                footage_keywords = topic.split()[:3]
                footage = self.download_footage(footage_keywords)
        else:
            # User provided specific keywords
            footage = self.download_footage(footage_keywords)
        
        # Step 4: Assemble video with text overlays
        video = self.assemble_video(voiceover, footage, script=script, ai_provider=ai_provider)
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


def interactive_mode():
    """Interactive mode with prompts for user input"""
    print("\n" + "=" * 60)
    print("FACELESS YOUTUBE VIDEO GENERATOR - INTERACTIVE MODE")
    print("=" * 60)
    
    # Show trending topics first
    print("\nWould you like to see trending topic suggestions? (y/n): ", end="")
    show_trends = input().strip().lower()
    if show_trends == 'y':
        get_trending_topics()
    
    # Get topic
    print("\nEnter your video topic: ", end="")
    topic = input().strip()
    if not topic:
        print("Error: Topic is required!")
        return 1
    
    # Get length
    print("Enter video length in minutes (default: 8): ", end="")
    length_input = input().strip()
    length = int(length_input) if length_input else 8
    
    # Get AI provider
    print("Choose AI provider (auto/groq/gemini/ollama, default: auto): ", end="")
    ai_provider = input().strip().lower() or 'auto'
    
    # Get keywords
    print("Enter footage keywords (comma-separated, or press Enter for auto): ", end="")
    keywords_input = input().strip()
    keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else None
    
    # Run generation
    generator = FacelessVideoGenerator()
    result = generator.run(
        topic=topic,
        length_minutes=length,
        footage_keywords=keywords,
        ai_provider=ai_provider
    )
    
    if result:
        print("\nYour video is ready!")
        print(f"Project directory: {result['project_dir']}")
        return 0
    else:
        print("\nVideo generation failed.")
        return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate faceless YouTube videos automatically',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python master_automation.py --topic "5 AI Tools for Productivity" --length 8
  python master_automation.py --suggest-topics
  python master_automation.py --interactive
  python master_automation.py -t "Investment Tips" -l 10 --ai groq

High CPM Niches (Better Monetization):
  - Finance: $15-$50 CPM
  - Business: $12-$35 CPM
  - Technology: $10-$30 CPM
  - Health: $10-$25 CPM
  - Education: $8-$20 CPM
        """
    )
    parser.add_argument(
        '--topic', '-t',
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
    parser.add_argument(
        '--ai',
        choices=['auto', 'groq', 'gemini', 'ollama'],
        default='auto',
        help='AI provider for script generation (default: auto)'
    )
    parser.add_argument(
        '--suggest-topics',
        action='store_true',
        help='Show trending topic suggestions with monetization focus'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode with prompts'
    )
    
    args = parser.parse_args()
    
    # Handle suggest-topics mode
    if args.suggest_topics:
        get_trending_topics()
        return 0
    
    # Handle interactive mode
    if args.interactive:
        return interactive_mode()
    
    # Require topic for normal mode
    if not args.topic:
        parser.print_help()
        print("\nError: --topic is required (or use --interactive or --suggest-topics)")
        return 1
    
    generator = FacelessVideoGenerator(project_name=args.project)
    result = generator.run(
        topic=args.topic,
        length_minutes=args.length,
        footage_keywords=args.keywords,
        ai_provider=args.ai
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
