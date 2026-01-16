# Module 5: Free AI Image and Video Generation Tools

## Overview

Visual content is the core of faceless YouTube videos. This module covers free tools and practical scripts to generate images, download stock footage, and create visual assets for your videos.

## Free Stock Footage Sources

### 1. Pexels (Best Overall)
- **Website**: https://www.pexels.com/videos/
- **License**: Free for commercial use, no attribution required
- **API**: Free API available for automation
- **Quality**: HD and 4K videos available

### 2. Pixabay
- **Website**: https://pixabay.com/videos/
- **License**: Free for commercial use
- **API**: Free API available
- **Quality**: HD videos, large library

### 3. Coverr
- **Website**: https://coverr.co/
- **License**: Free for commercial use
- **Quality**: High-quality cinematic footage

### 4. Videvo
- **Website**: https://www.videvo.net/
- **License**: Mix of free and premium
- **Quality**: Good variety of footage

### 5. Mixkit
- **Website**: https://mixkit.co/free-stock-video/
- **License**: Free for commercial use
- **Quality**: Professional quality clips

### 6. Life of Vids
- **Website**: https://lifeofvids.com/
- **License**: Free, no copyright restrictions
- **Quality**: Artistic, cinematic clips

## Practical Script: Automated Stock Footage Downloader

### Setup Requirements

```bash
pip install requests pexels-api python-dotenv
```

### Pexels API Downloader Script

```python
#!/usr/bin/env python3
"""
Pexels Stock Footage Downloader
Automatically downloads relevant stock videos for your content
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get free API key from: https://www.pexels.com/api/
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', 'YOUR_API_KEY_HERE')

class PexelsDownloader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/videos"
        self.headers = {"Authorization": api_key}
    
    def search_videos(self, query, per_page=10, orientation="landscape"):
        """Search for videos matching the query"""
        params = {
            "query": query,
            "per_page": per_page,
            "orientation": orientation
        }
        response = requests.get(
            f"{self.base_url}/search",
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def download_video(self, video_url, output_path):
        """Download a video from URL"""
        response = requests.get(video_url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {output_path}")
    
    def get_best_quality_link(self, video_files):
        """Get the highest quality video link"""
        # Sort by height (quality) and get the best one
        sorted_files = sorted(video_files, key=lambda x: x.get('height', 0), reverse=True)
        for file in sorted_files:
            if file.get('quality') == 'hd' or file.get('height', 0) >= 720:
                return file.get('link')
        return sorted_files[0].get('link') if sorted_files else None
    
    def download_videos_for_topic(self, topic, num_videos=5, output_dir="downloads"):
        """Download multiple videos for a topic"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = self.search_videos(topic, per_page=num_videos)
        videos = results.get('videos', [])
        
        downloaded = []
        for i, video in enumerate(videos):
            video_files = video.get('video_files', [])
            video_url = self.get_best_quality_link(video_files)
            
            if video_url:
                filename = f"{topic.replace(' ', '_')}_{i+1}.mp4"
                output_path = os.path.join(output_dir, filename)
                self.download_video(video_url, output_path)
                downloaded.append(output_path)
        
        return downloaded


def main():
    # Example usage
    downloader = PexelsDownloader(PEXELS_API_KEY)
    
    # Download videos for different topics
    topics = [
        "business office",
        "technology computer",
        "nature landscape",
        "city aerial",
        "money finance"
    ]
    
    for topic in topics:
        print(f"\nDownloading videos for: {topic}")
        downloaded = downloader.download_videos_for_topic(
            topic, 
            num_videos=3, 
            output_dir=f"stock_footage/{topic.replace(' ', '_')}"
        )
        print(f"Downloaded {len(downloaded)} videos")


if __name__ == "__main__":
    main()
```

### Pixabay Downloader Script

```python
#!/usr/bin/env python3
"""
Pixabay Stock Footage Downloader
Free alternative to Pexels
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get free API key from: https://pixabay.com/api/docs/
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', 'YOUR_API_KEY_HERE')

class PixabayDownloader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api/videos/"
    
    def search_videos(self, query, per_page=10):
        """Search for videos"""
        params = {
            "key": self.api_key,
            "q": query,
            "per_page": per_page,
            "video_type": "all"
        }
        response = requests.get(self.base_url, params=params)
        return response.json()
    
    def download_video(self, video_url, output_path):
        """Download video from URL"""
        response = requests.get(video_url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {output_path}")
    
    def download_videos_for_topic(self, topic, num_videos=5, output_dir="downloads"):
        """Download videos for a topic"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = self.search_videos(topic, per_page=num_videos)
        hits = results.get('hits', [])
        
        downloaded = []
        for i, video in enumerate(hits):
            # Get medium quality (free tier)
            videos = video.get('videos', {})
            medium = videos.get('medium', {})
            video_url = medium.get('url')
            
            if video_url:
                filename = f"{topic.replace(' ', '_')}_{i+1}.mp4"
                output_path = os.path.join(output_dir, filename)
                self.download_video(video_url, output_path)
                downloaded.append(output_path)
        
        return downloaded


if __name__ == "__main__":
    downloader = PixabayDownloader(PIXABAY_API_KEY)
    downloaded = downloader.download_videos_for_topic("technology", num_videos=3)
    print(f"Downloaded {len(downloaded)} videos")
```

## Free AI Image Generation Tools

### 1. Stable Diffusion (Local, Free)
- Run locally on your computer
- No usage limits
- Requires decent GPU (or use CPU with patience)

### 2. DALL-E (Limited Free)
- OpenAI's image generator
- Limited free credits
- High quality results

### 3. Bing Image Creator (Free)
- Microsoft's DALL-E powered tool
- Free with Microsoft account
- Good quality

### 4. Leonardo.ai (Free Tier)
- 150 free images per day
- Good for thumbnails and graphics

### 5. Canva AI (Free Tier)
- Built into Canva
- Good for quick graphics

### 6. Ideogram (Free)
- Good for text in images
- Free tier available

## Practical Script: AI Image Generation with Stable Diffusion

### Local Setup (Requires GPU)

```bash
pip install diffusers transformers accelerate torch
```

### Stable Diffusion Script

```python
#!/usr/bin/env python3
"""
Stable Diffusion Image Generator
Generate custom images for your videos locally
"""

import torch
from diffusers import StableDiffusionPipeline
import os

class ImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        """Initialize the Stable Diffusion pipeline"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load model (downloads on first run ~4GB)
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        self.pipe = self.pipe.to(self.device)
    
    def generate_image(self, prompt, output_path, 
                       negative_prompt="blurry, bad quality, distorted",
                       num_inference_steps=50,
                       guidance_scale=7.5):
        """Generate an image from a text prompt"""
        
        image = self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale
        ).images[0]
        
        image.save(output_path)
        print(f"Generated: {output_path}")
        return output_path
    
    def generate_batch(self, prompts, output_dir="generated_images"):
        """Generate multiple images"""
        os.makedirs(output_dir, exist_ok=True)
        
        generated = []
        for i, prompt in enumerate(prompts):
            output_path = os.path.join(output_dir, f"image_{i+1}.png")
            self.generate_image(prompt, output_path)
            generated.append(output_path)
        
        return generated


# Example prompts for different video types
THUMBNAIL_PROMPTS = {
    "finance": "professional business person looking at stock charts, modern office, dramatic lighting, 4k, detailed",
    "tech": "futuristic technology concept, glowing circuits, blue neon lights, high tech, 4k render",
    "motivation": "person standing on mountain peak at sunrise, epic landscape, inspirational, cinematic",
    "education": "open book with magical glowing knowledge symbols, fantasy style, detailed illustration",
    "health": "healthy lifestyle concept, fresh vegetables and exercise equipment, bright clean aesthetic"
}

if __name__ == "__main__":
    # Note: This requires a GPU with at least 4GB VRAM
    # For CPU-only, it will be very slow but still work
    
    generator = ImageGenerator()
    
    # Generate a single image
    generator.generate_image(
        prompt=THUMBNAIL_PROMPTS["tech"],
        output_path="tech_thumbnail.png"
    )
```

## Thumbnail Creation with Canva API Alternative

### Using Pillow for Thumbnail Creation

```python
#!/usr/bin/env python3
"""
Thumbnail Generator
Create YouTube thumbnails programmatically
"""

from PIL import Image, ImageDraw, ImageFont
import os

class ThumbnailGenerator:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
    
    def create_thumbnail(self, background_image, title_text, output_path,
                        font_size=80, text_color=(255, 255, 255),
                        overlay_color=(0, 0, 0, 128)):
        """Create a thumbnail with text overlay"""
        
        # Open and resize background
        img = Image.open(background_image)
        img = img.resize((self.width, self.height), Image.LANCZOS)
        
        # Add dark overlay for text readability
        overlay = Image.new('RGBA', (self.width, self.height), overlay_color)
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        
        # Add text
        draw = ImageDraw.Draw(img)
        
        # Try to use a bold font, fall back to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw text with shadow
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), title_text, 
                  font=font, fill=(0, 0, 0, 200))
        draw.text((x, y), title_text, font=font, fill=text_color)
        
        # Save
        img = img.convert('RGB')
        img.save(output_path, quality=95)
        print(f"Created thumbnail: {output_path}")
        return output_path
    
    def create_gradient_thumbnail(self, title_text, output_path,
                                  colors=[(102, 126, 234), (118, 75, 162)],
                                  font_size=80):
        """Create a thumbnail with gradient background"""
        
        # Create gradient
        img = Image.new('RGB', (self.width, self.height))
        
        for y in range(self.height):
            ratio = y / self.height
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            
            for x in range(self.width):
                img.putpixel((x, y), (r, g, b))
        
        # Add text
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Word wrap for long titles
        words = title_text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > self.width - 100:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw each line
        total_height = len(lines) * (font_size + 10)
        start_y = (self.height - total_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            y = start_y + i * (font_size + 10)
            
            # Shadow
            draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0))
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        img.save(output_path, quality=95)
        print(f"Created thumbnail: {output_path}")
        return output_path


if __name__ == "__main__":
    generator = ThumbnailGenerator()
    
    # Create gradient thumbnail
    generator.create_gradient_thumbnail(
        title_text="10 AI Tools That Will Change Your Life",
        output_path="thumbnail_gradient.jpg"
    )
```

## Batch Content Preparation Script

```python
#!/usr/bin/env python3
"""
Batch Content Preparation
Prepare all visual assets for a video automatically
"""

import os
import json
from datetime import datetime

class ContentPreparer:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.dirs = {
            'scripts': os.path.join(project_dir, 'scripts'),
            'voiceovers': os.path.join(project_dir, 'voiceovers'),
            'footage': os.path.join(project_dir, 'footage'),
            'thumbnails': os.path.join(project_dir, 'thumbnails'),
            'output': os.path.join(project_dir, 'output')
        }
        
        # Create all directories
        for dir_path in self.dirs.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def create_project_structure(self, video_title, script_sections):
        """Create a complete project structure for a video"""
        
        # Create project manifest
        manifest = {
            'title': video_title,
            'created': datetime.now().isoformat(),
            'sections': script_sections,
            'status': {
                'script': 'pending',
                'voiceover': 'pending',
                'footage': 'pending',
                'thumbnail': 'pending',
                'editing': 'pending',
                'upload': 'pending'
            }
        }
        
        # Save manifest
        manifest_path = os.path.join(self.project_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Create section files
        for i, section in enumerate(script_sections):
            section_file = os.path.join(self.dirs['scripts'], f'section_{i+1}.txt')
            with open(section_file, 'w') as f:
                f.write(section)
        
        print(f"Project structure created at: {self.project_dir}")
        return manifest
    
    def get_footage_keywords(self, script_text):
        """Extract keywords for stock footage search"""
        # Simple keyword extraction (can be enhanced with NLP)
        common_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 
                       'been', 'being', 'have', 'has', 'had', 'do', 'does',
                       'did', 'will', 'would', 'could', 'should', 'may',
                       'might', 'must', 'shall', 'can', 'need', 'dare',
                       'ought', 'used', 'to', 'of', 'in', 'for', 'on',
                       'with', 'at', 'by', 'from', 'as', 'into', 'through',
                       'during', 'before', 'after', 'above', 'below', 'between',
                       'under', 'again', 'further', 'then', 'once', 'here',
                       'there', 'when', 'where', 'why', 'how', 'all', 'each',
                       'few', 'more', 'most', 'other', 'some', 'such', 'no',
                       'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                       'too', 'very', 'just', 'and', 'but', 'if', 'or',
                       'because', 'until', 'while', 'this', 'that', 'these',
                       'those', 'what', 'which', 'who', 'whom', 'your', 'you'}
        
        words = script_text.lower().split()
        keywords = [w.strip('.,!?;:') for w in words 
                   if w.strip('.,!?;:') not in common_words and len(w) > 3]
        
        # Get unique keywords, preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)
        
        return unique_keywords[:10]  # Return top 10 keywords


if __name__ == "__main__":
    # Example usage
    preparer = ContentPreparer("my_video_project")
    
    sections = [
        "Welcome to today's video about productivity tips that will transform your work life.",
        "The first tip is to start your day with the most important task, also known as eating the frog.",
        "Second, eliminate all distractions during your deep work sessions.",
        "Third, use the Pomodoro technique to maintain focus and take regular breaks.",
        "Thanks for watching! Subscribe for more productivity content."
    ]
    
    manifest = preparer.create_project_structure(
        video_title="5 Productivity Tips That Changed My Life",
        script_sections=sections
    )
    
    # Get footage keywords for first section
    keywords = preparer.get_footage_keywords(sections[0])
    print(f"Suggested footage keywords: {keywords}")
```

## Quality Checklist for Visual Assets

Before using any visual content, verify:

- [ ] Resolution is at least 1080p (1920x1080)
- [ ] No watermarks or logos
- [ ] License allows commercial use
- [ ] Content matches your script
- [ ] Colors and style are consistent
- [ ] No copyrighted material visible
- [ ] Thumbnail is eye-catching and readable

## Next Steps

1. Get free API keys from Pexels and Pixabay
2. Run the stock footage downloader for your niche
3. Create your first thumbnail using the generator
4. Set up a project structure for your first video
5. Move to Module 6 for video editing automation

---

## Additional Resources

- [Pexels API](https://www.pexels.com/api/) - Free stock footage API
- [Pixabay API](https://pixabay.com/api/docs/) - Free stock footage API
- [Stable Diffusion](https://github.com/CompVis/stable-diffusion) - Open source image generation
- [Pillow Documentation](https://pillow.readthedocs.io/) - Python imaging library
- [Leonardo.ai](https://leonardo.ai/) - Free AI image generation
