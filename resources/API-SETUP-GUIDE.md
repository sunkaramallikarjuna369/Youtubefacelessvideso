# Complete API Setup Guide - Zero Cost Strategy

This guide covers all the APIs and tools you need for automated faceless YouTube video creation, prioritizing **completely free** options.

## Cost Optimization Strategy

### Tier 1: 100% Free (No Cost Ever)
These tools have no usage limits and cost nothing:

| Tool | Purpose | Limits |
|------|---------|--------|
| Ollama | AI Script Writing | Unlimited (runs locally) |
| Edge TTS | Voice Generation | Unlimited |
| Pexels API | Stock Footage | 200 requests/hour |
| Pixabay API | Stock Footage | 5000 requests/hour |
| DaVinci Resolve | Video Editing | Full features free |
| MoviePy | Video Editing (Python) | Unlimited |
| Pillow | Thumbnail Creation | Unlimited |
| GIMP | Image Editing | Full features free |

### Tier 2: Free Tier (Generous Limits)
These have free tiers sufficient for beginners:

| Tool | Purpose | Free Limit |
|------|---------|------------|
| Google Gemini API | AI Script Writing | 60 requests/minute |
| Groq API | Fast AI Inference | Free tier available |
| YouTube Data API | Video Uploads | 10,000 units/day |
| Canva | Thumbnails | Limited free features |

### Tier 3: Pay Later (When Earning)
Only consider these after you're monetized:

| Tool | Purpose | Starting Cost |
|------|---------|---------------|
| ElevenLabs | Premium Voice | $5/month |
| Midjourney | AI Images | $10/month |
| OpenAI API | GPT-4 | Pay per use |

---

## 1. Ollama Setup (FREE Local LLM)

Ollama lets you run powerful AI models locally with **zero cost and no limits**.

### Installation

**Linux/WSL:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Download from https://ollama.com/download

### Download Models

```bash
# Recommended models for script writing
ollama pull llama3.1:8b      # Best balance of speed/quality
ollama pull mistral          # Fast and capable
ollama pull gemma2:9b        # Google's model

# For lower-end computers
ollama pull phi3:mini        # Small but capable
ollama pull tinyllama        # Very fast, basic tasks
```

### Python Integration

```python
#!/usr/bin/env python3
"""
Ollama Script Generator - 100% Free, No Limits
"""

import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, prompt, model="llama3.1:8b", stream=False):
        """Generate text using Ollama"""
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": stream
            }
        )
        
        if stream:
            return response.iter_lines()
        else:
            return response.json().get('response', '')
    
    def chat(self, messages, model="llama3.1:8b"):
        """Chat completion with Ollama"""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False
            }
        )
        return response.json().get('message', {}).get('content', '')
    
    def generate_script(self, topic, video_length_minutes=8):
        """Generate a complete YouTube script"""
        word_count = video_length_minutes * 150
        
        prompt = f"""Write a YouTube video script about: {topic}

Requirements:
- Approximately {word_count} words ({video_length_minutes} minutes when spoken)
- Start with an attention-grabbing hook
- Include 4-5 main points with examples
- Add [VISUAL CUE] markers for B-roll suggestions
- End with a call to action
- Conversational, engaging tone

Write the complete script now:"""
        
        return self.generate(prompt)
    
    def improve_script(self, script):
        """Improve an existing script"""
        prompt = f"""Improve this YouTube script to be more engaging:

{script}

Make it:
- More conversational
- Add better hooks and transitions
- Include specific examples
- Add pattern interrupts

Improved script:"""
        
        return self.generate(prompt)


# Example usage
if __name__ == "__main__":
    client = OllamaClient()
    
    # Generate a script
    script = client.generate_script(
        topic="5 Free AI Tools That Will Save You Hours Every Week",
        video_length_minutes=8
    )
    print(script)
```

### Start Ollama Server

```bash
# Start the server (run in background)
ollama serve &

# Or run a model directly (starts server automatically)
ollama run llama3.1:8b
```

---

## 2. Google Gemini API (FREE Tier)

Google's Gemini offers a generous free tier perfect for script writing.

### Get API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and save your key

### Python Integration

```python
#!/usr/bin/env python3
"""
Google Gemini Script Generator - Free Tier
60 requests/minute, 1500 requests/day
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Free tier model
    
    def generate(self, prompt):
        """Generate text using Gemini"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_script(self, topic, video_length_minutes=8):
        """Generate a YouTube script"""
        word_count = video_length_minutes * 150
        
        prompt = f"""Create a YouTube video script about: {topic}

Requirements:
- Length: approximately {word_count} words
- Hook in first 10 seconds
- 4-5 main sections with transitions
- [VISUAL] markers for B-roll
- Engaging, conversational tone
- Strong call to action at end

Write the complete script:"""
        
        return self.generate(prompt)
    
    def generate_video_ideas(self, niche, count=10):
        """Generate video ideas for a niche"""
        prompt = f"""Generate {count} viral YouTube video ideas for the {niche} niche.

For each idea provide:
1. Title (optimized for clicks)
2. Brief description
3. Target audience
4. Estimated appeal (1-10)

Format as a numbered list:"""
        
        return self.generate(prompt)


# Installation: pip install google-generativeai python-dotenv

if __name__ == "__main__":
    client = GeminiClient()
    
    # Generate video ideas
    ideas = client.generate_video_ideas("personal finance", count=5)
    print(ideas)
```

---

## 3. Groq API (FREE Fast Inference)

Groq offers extremely fast AI inference with a free tier.

### Get API Key

1. Go to https://console.groq.com/
2. Sign up for free account
3. Go to API Keys section
4. Create new API key

### Python Integration

```python
#!/usr/bin/env python3
"""
Groq Fast AI - Free Tier
Very fast inference, great for batch processing
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, messages, model="llama-3.1-70b-versatile"):
        """Chat completion with Groq"""
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4096
            }
        )
        return response.json()['choices'][0]['message']['content']
    
    def generate_script(self, topic):
        """Generate a script using Groq"""
        messages = [
            {
                "role": "system",
                "content": "You are an expert YouTube scriptwriter. Write engaging, conversational scripts with hooks, transitions, and calls to action."
            },
            {
                "role": "user",
                "content": f"Write an 8-minute YouTube script about: {topic}"
            }
        ]
        return self.chat(messages)


# Installation: pip install requests python-dotenv

if __name__ == "__main__":
    client = GroqClient()
    script = client.generate_script("How to Start a Side Hustle in 2024")
    print(script)
```

---

## 4. Edge TTS (100% FREE Voice)

Microsoft Edge TTS is completely free with no limits.

### Installation

```bash
pip install edge-tts
```

### Python Integration

```python
#!/usr/bin/env python3
"""
Edge TTS Voice Generator - 100% Free, Unlimited
"""

import edge_tts
import asyncio
import os

class VoiceGenerator:
    # Best voices for YouTube
    VOICES = {
        'male_us': 'en-US-GuyNeural',
        'female_us': 'en-US-JennyNeural',
        'male_uk': 'en-GB-RyanNeural',
        'female_uk': 'en-GB-SoniaNeural',
        'male_au': 'en-AU-WilliamNeural',
        'female_au': 'en-AU-NatashaNeural',
    }
    
    def __init__(self, voice='male_us'):
        self.voice = self.VOICES.get(voice, voice)
    
    async def _generate(self, text, output_file):
        """Internal async generation"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)
    
    def generate(self, text, output_file):
        """Generate voice from text"""
        asyncio.run(self._generate(text, output_file))
        print(f"Generated: {output_file}")
        return output_file
    
    def generate_from_script(self, script_file, output_file):
        """Generate voice from script file"""
        with open(script_file, 'r') as f:
            text = f.read()
        return self.generate(text, output_file)
    
    def batch_generate(self, sections, output_dir):
        """Generate voice for multiple sections"""
        os.makedirs(output_dir, exist_ok=True)
        outputs = []
        
        for i, section in enumerate(sections):
            output_file = os.path.join(output_dir, f"section_{i+1}.mp3")
            self.generate(section, output_file)
            outputs.append(output_file)
        
        return outputs
    
    @staticmethod
    def list_voices():
        """List all available voices"""
        async def get_voices():
            voices = await edge_tts.list_voices()
            return voices
        return asyncio.run(get_voices())


if __name__ == "__main__":
    generator = VoiceGenerator(voice='male_us')
    
    # Generate single file
    generator.generate(
        "Welcome to today's video about making money online.",
        "intro.mp3"
    )
    
    # Batch generate
    sections = [
        "Welcome to today's video.",
        "Let's dive into our first topic.",
        "Thanks for watching, don't forget to subscribe!"
    ]
    generator.batch_generate(sections, "voiceovers")
```

---

## 5. Pexels API (FREE Stock Footage)

### Get API Key

1. Go to https://www.pexels.com/api/
2. Click "Get Started"
3. Create free account
4. Copy your API key

### Python Integration

```python
#!/usr/bin/env python3
"""
Pexels Stock Footage Downloader - Free API
200 requests/hour, 20,000 requests/month
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PexelsClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('PEXELS_API_KEY')
        self.headers = {"Authorization": self.api_key}
        self.base_url = "https://api.pexels.com"
    
    def search_videos(self, query, per_page=10):
        """Search for videos"""
        response = requests.get(
            f"{self.base_url}/videos/search",
            headers=self.headers,
            params={"query": query, "per_page": per_page}
        )
        return response.json()
    
    def search_photos(self, query, per_page=10):
        """Search for photos"""
        response = requests.get(
            f"{self.base_url}/v1/search",
            headers=self.headers,
            params={"query": query, "per_page": per_page}
        )
        return response.json()
    
    def download_video(self, video_data, output_dir):
        """Download a video"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Get best quality
        video_files = video_data.get('video_files', [])
        best = max(video_files, key=lambda x: x.get('height', 0))
        
        url = best.get('link')
        filename = f"video_{video_data['id']}.mp4"
        output_path = os.path.join(output_dir, filename)
        
        response = requests.get(url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {output_path}")
        return output_path
    
    def download_videos_for_topic(self, topic, count=5, output_dir="footage"):
        """Download multiple videos for a topic"""
        results = self.search_videos(topic, per_page=count)
        videos = results.get('videos', [])
        
        downloaded = []
        for video in videos:
            path = self.download_video(video, output_dir)
            downloaded.append(path)
        
        return downloaded


if __name__ == "__main__":
    client = PexelsClient()
    
    # Download footage for different topics
    topics = ["business meeting", "technology", "nature"]
    for topic in topics:
        client.download_videos_for_topic(topic, count=3, output_dir=f"footage/{topic}")
```

---

## 6. Pixabay API (FREE Stock Footage)

### Get API Key

1. Go to https://pixabay.com/api/docs/
2. Create free account
3. Your API key is shown on the documentation page

### Python Integration

```python
#!/usr/bin/env python3
"""
Pixabay Stock Footage - Free API
5000 requests/hour
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

class PixabayClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('PIXABAY_API_KEY')
        self.base_url = "https://pixabay.com/api"
    
    def search_videos(self, query, per_page=10):
        """Search for videos"""
        response = requests.get(
            f"{self.base_url}/videos/",
            params={
                "key": self.api_key,
                "q": query,
                "per_page": per_page
            }
        )
        return response.json()
    
    def search_images(self, query, per_page=10):
        """Search for images"""
        response = requests.get(
            f"{self.base_url}/",
            params={
                "key": self.api_key,
                "q": query,
                "per_page": per_page,
                "image_type": "photo"
            }
        )
        return response.json()
    
    def download_video(self, video_data, output_dir):
        """Download a video"""
        os.makedirs(output_dir, exist_ok=True)
        
        videos = video_data.get('videos', {})
        # Get medium quality (free tier)
        url = videos.get('medium', {}).get('url')
        
        if not url:
            url = videos.get('small', {}).get('url')
        
        filename = f"video_{video_data['id']}.mp4"
        output_path = os.path.join(output_dir, filename)
        
        response = requests.get(url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {output_path}")
        return output_path


if __name__ == "__main__":
    client = PixabayClient()
    results = client.search_videos("office work", per_page=3)
    
    for video in results.get('hits', []):
        client.download_video(video, "pixabay_footage")
```

---

## 7. YouTube Data API (FREE Uploads)

### Get API Key & OAuth Credentials

1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Download credentials JSON file

### Python Integration

```python
#!/usr/bin/env python3
"""
YouTube Upload Automation
Free: 10,000 quota units/day (uploads cost 1600 units each = ~6 uploads/day)
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, credentials_file='client_secrets.json'):
        self.credentials_file = credentials_file
        self.youtube = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API"""
        creds = None
        
        # Load saved credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('youtube', 'v3', credentials=creds)
    
    def upload_video(self, video_file, title, description, tags=None, 
                     category_id='22', privacy='private'):
        """Upload a video to YouTube"""
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy,  # 'private', 'unlisted', 'public'
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(
            video_file,
            mimetype='video/mp4',
            resumable=True
        )
        
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = request.execute()
        video_id = response['id']
        print(f"Uploaded: https://youtube.com/watch?v={video_id}")
        return video_id
    
    def set_thumbnail(self, video_id, thumbnail_file):
        """Set custom thumbnail for a video"""
        self.youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_file)
        ).execute()
        print(f"Thumbnail set for video: {video_id}")


# Installation: pip install google-auth-oauthlib google-api-python-client

if __name__ == "__main__":
    uploader = YouTubeUploader()
    
    video_id = uploader.upload_video(
        video_file="final_video.mp4",
        title="10 AI Tools That Will Change Your Life",
        description="In this video, we explore 10 amazing AI tools...",
        tags=["AI", "productivity", "tools", "technology"],
        privacy="private"  # Start private, then make public after review
    )
```

---

## Environment Setup (.env file)

Create a `.env` file in your project root:

```env
# Free APIs
PEXELS_API_KEY=your_pexels_key_here
PIXABAY_API_KEY=your_pixabay_key_here
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here

# YouTube (OAuth - use credentials file instead)
# YOUTUBE_CLIENT_ID=your_client_id
# YOUTUBE_CLIENT_SECRET=your_client_secret
```

---

## Quick Start Checklist

### Day 1: Set Up Free Tools
- [ ] Install Ollama and download llama3.1:8b model
- [ ] Install Edge TTS (`pip install edge-tts`)
- [ ] Get Pexels API key (free)
- [ ] Get Pixabay API key (free)

### Day 2: Set Up Optional Free Tiers
- [ ] Get Google Gemini API key (free tier)
- [ ] Get Groq API key (free tier)
- [ ] Set up YouTube API credentials

### Day 3: Test Everything
- [ ] Generate a test script with Ollama
- [ ] Generate a test voiceover with Edge TTS
- [ ] Download test footage from Pexels
- [ ] Run the complete pipeline

---

## Cost Summary

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| Ollama | $0 | Runs locally |
| Edge TTS | $0 | Unlimited |
| Pexels API | $0 | 200 req/hour |
| Pixabay API | $0 | 5000 req/hour |
| Gemini API | $0 | Free tier |
| Groq API | $0 | Free tier |
| YouTube API | $0 | Free |
| DaVinci Resolve | $0 | Free version |
| **TOTAL** | **$0** | Everything free! |

You can create unlimited faceless YouTube videos with **zero cost** using these tools!
