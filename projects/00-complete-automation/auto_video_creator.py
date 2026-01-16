"""
KRWUTARTH'S COMPLETE YOUTUBE AUTOMATION SYSTEM
==============================================
This script does EVERYTHING automatically:
1. Finds trending topics
2. Generates video script with AI
3. Creates voiceover
4. Downloads video clips
5. Assembles the final video
6. Creates thumbnail
7. Uploads to YouTube

NO MANUAL INTERVENTION REQUIRED!
Just run once and it handles everything.

Requirements (install once):
pip install edge-tts moviepy pillow google-api-python-client google-auth-oauthlib pytrends requests

For Windows: Make sure Ollama is running (ollama serve)
"""

import os
import sys
import json
import asyncio
import random
import datetime
import pickle
from pathlib import Path

# Auto-install missing packages
def install_package(package):
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

# Check and install required packages
required_packages = {
    'edge_tts': 'edge-tts',
    'moviepy': 'moviepy',
    'PIL': 'pillow',
    'pytrends': 'pytrends',
    'requests': 'requests',
    'googleapiclient': 'google-api-python-client',
    'google_auth_oauthlib': 'google-auth-oauthlib',
}

for module, package in required_packages.items():
    try:
        __import__(module.split('.')[0])
    except ImportError:
        print(f"Installing {package}...")
        install_package(package)

import requests
import edge_tts
from pytrends.request import TrendReq

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, ColorClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("WARNING: MoviePy not available. Video assembly will be skipped.")

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False
    print("WARNING: YouTube API not available. Upload will be skipped.")

# Import config
from config import *


class YouTubeAutomation:
    """Complete YouTube Video Automation System"""
    
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
        self.ensure_output_folder()
        self.trending_topic = None
        self.script = None
        self.voiceover_file = None
        self.video_clips = []
        self.final_video = None
        self.thumbnail_file = None
        self.metadata = {}
        
    def ensure_output_folder(self):
        """Create output folder if it doesn't exist"""
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(os.path.join(self.output_folder, "clips"), exist_ok=True)
        
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "=" * 70)
        print("   KRWUTARTH'S COMPLETE YOUTUBE AUTOMATION SYSTEM")
        print("   Zero Manual Intervention - 100% Automatic!")
        print("=" * 70 + "\n")
        
    def print_step(self, step_num, message):
        """Print step progress"""
        print(f"\n[STEP {step_num}/7] {message}")
        print("-" * 50)
        
    # =========================================
    # STEP 1: TREND DISCOVERY
    # =========================================
    def discover_trends(self):
        """Find trending topics using Google Trends"""
        self.print_step(1, "DISCOVERING TRENDING TOPICS...")
        
        try:
            # Initialize pytrends
            pytrends = TrendReq(hl='en-US', tz=360)
            
            # Get trending searches
            trending_searches = pytrends.trending_searches(pn='united_states')
            trends_list = trending_searches[0].tolist()[:NUM_TRENDS_TO_CHECK]
            
            print(f"  Found {len(trends_list)} trending topics!")
            
            # Filter trends based on niche keywords
            relevant_trends = []
            for trend in trends_list:
                trend_lower = trend.lower()
                # Check if trend is relevant to niche
                for keyword in NICHE_KEYWORDS:
                    if keyword.lower() in trend_lower:
                        relevant_trends.append(trend)
                        break
            
            # If no relevant trends, use general trends
            if not relevant_trends:
                relevant_trends = trends_list[:5]
                print(f"  Using general trends (no niche-specific found)")
            else:
                print(f"  Found {len(relevant_trends)} niche-relevant trends!")
            
            # Pick a random trend from top relevant ones
            self.trending_topic = random.choice(relevant_trends[:5])
            print(f"\n  SELECTED TOPIC: {self.trending_topic}")
            
            return self.trending_topic
            
        except Exception as e:
            print(f"  WARNING: Could not fetch trends: {e}")
            # Fallback to predefined topics based on niche
            fallback_topics = self.get_fallback_topics()
            self.trending_topic = random.choice(fallback_topics)
            print(f"  Using fallback topic: {self.trending_topic}")
            return self.trending_topic
    
    def get_fallback_topics(self):
        """Get fallback topics based on niche"""
        topics = {
            "animals": [
                "5 Amazing Facts About Dolphins",
                "The Most Dangerous Animals in the World",
                "Cute Baby Animals That Will Melt Your Heart",
                "Animals With Superpowers",
                "The Smartest Animals on Earth"
            ],
            "space": [
                "5 Mind-Blowing Facts About Black Holes",
                "What Would Happen If You Fell Into a Black Hole",
                "The Biggest Stars in the Universe",
                "Mysterious Planets Scientists Can't Explain",
                "Amazing Facts About Mars"
            ],
            "gaming": [
                "5 Minecraft Tips Pro Players Use",
                "Hidden Secrets in Popular Video Games",
                "The Most Expensive Video Games Ever Made",
                "Gaming World Records That Seem Impossible",
                "Easter Eggs You Missed in Your Favorite Games"
            ],
            "science": [
                "5 Science Experiments That Went Wrong",
                "Mind-Blowing Science Facts",
                "Inventions That Changed the World",
                "The Weirdest Scientific Discoveries",
                "Science Facts That Sound Fake But Are True"
            ],
            "amazing facts": [
                "5 Facts That Will Blow Your Mind",
                "Things You Didn't Know About Everyday Objects",
                "The Most Unbelievable World Records",
                "Facts That Sound Fake But Are 100% True",
                "Mind-Blowing Facts About the Human Body"
            ]
        }
        
        # Get topics for current niche or default
        niche_lower = CHANNEL_NICHE.lower()
        for key in topics:
            if key in niche_lower:
                return topics[key]
        return topics["amazing facts"]
    
    # =========================================
    # STEP 2: AI SCRIPT GENERATION
    # =========================================
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_script(self):
        """Generate video script using Ollama AI"""
        self.print_step(2, "GENERATING VIDEO SCRIPT WITH AI...")
        
        if not self.check_ollama():
            print("  ERROR: Ollama is not running!")
            print("  Please start Ollama with: ollama serve")
            print("  Then run this script again.")
            return None
        
        # Create prompt for script generation
        prompt = f"""Write an engaging YouTube video script about: {self.trending_topic}

Requirements:
- Start with an exciting hook to grab attention
- Include exactly {NUM_FACTS} amazing facts or points
- Each fact should be interesting and surprising
- Use simple language that anyone can understand
- Be enthusiastic and energetic
- Total length should be about 2-3 minutes when read aloud
- End with a call to action (like, subscribe, comment)

Format:
[INTRO]
(Write the intro here)

[FACT 1]
(Write fact 1 here)

[FACT 2]
(Write fact 2 here)

... and so on

[OUTRO]
(Write the outro here)

Make it exciting and fun to watch!"""

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=180
            )
            
            if response.status_code == 200:
                self.script = response.json().get('response', '')
                
                # Save script to file
                script_file = os.path.join(self.output_folder, "script.txt")
                with open(script_file, "w", encoding="utf-8") as f:
                    f.write(f"Topic: {self.trending_topic}\n")
                    f.write(f"Generated: {datetime.datetime.now()}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(self.script)
                
                print(f"  Script generated! ({len(self.script)} characters)")
                print(f"  Saved to: {script_file}")
                return self.script
            else:
                print(f"  ERROR: Ollama returned status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ERROR generating script: {e}")
            return None
    
    # =========================================
    # STEP 3: VOICEOVER GENERATION
    # =========================================
    async def generate_voiceover_async(self):
        """Generate voiceover using Edge TTS"""
        self.print_step(3, "CREATING VOICEOVER...")
        
        if not self.script:
            print("  ERROR: No script available!")
            return None
        
        # Clean script for voiceover (remove formatting markers)
        clean_script = self.script
        for marker in ['[INTRO]', '[OUTRO]', '[FACT 1]', '[FACT 2]', '[FACT 3]', 
                       '[FACT 4]', '[FACT 5]', '[FACT 6]', '[FACT 7]', '[FACT 8]',
                       '[FACT 9]', '[FACT 10]']:
            clean_script = clean_script.replace(marker, '')
        
        self.voiceover_file = os.path.join(self.output_folder, "voiceover.mp3")
        
        try:
            # Create voiceover with Edge TTS
            communicate = edge_tts.Communicate(clean_script, VOICE)
            await communicate.save(self.voiceover_file)
            
            print(f"  Voiceover created!")
            print(f"  Saved to: {self.voiceover_file}")
            return self.voiceover_file
            
        except Exception as e:
            print(f"  ERROR creating voiceover: {e}")
            return None
    
    def generate_voiceover(self):
        """Wrapper for async voiceover generation"""
        return asyncio.run(self.generate_voiceover_async())
    
    # =========================================
    # STEP 4: VIDEO CLIPS DOWNLOAD
    # =========================================
    def download_video_clips(self):
        """Download video clips from Pexels"""
        self.print_step(4, "DOWNLOADING VIDEO CLIPS...")
        
        if PEXELS_API_KEY == "YOUR_PEXELS_API_KEY_HERE":
            print("  WARNING: No Pexels API key configured!")
            print("  Get your free key at: https://www.pexels.com/api/")
            print("  Add it to config.py")
            return []
        
        # Generate search terms based on topic
        search_terms = self.generate_search_terms()
        print(f"  Search terms: {search_terms[:3]}")
        
        clips_folder = os.path.join(self.output_folder, "clips")
        os.makedirs(clips_folder, exist_ok=True)
        
        downloaded_clips = []
        clips_needed = NUM_FACTS + 2  # Extra clips for intro/outro
        
        for term in search_terms:
            if len(downloaded_clips) >= clips_needed:
                break
                
            try:
                response = requests.get(
                    "https://api.pexels.com/videos/search",
                    headers={"Authorization": PEXELS_API_KEY},
                    params={
                        "query": term,
                        "per_page": 3,
                        "orientation": "landscape",
                        "size": "medium"
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    videos = response.json().get("videos", [])
                    
                    for video in videos:
                        if len(downloaded_clips) >= clips_needed:
                            break
                            
                        # Find HD video file
                        video_files = video.get("video_files", [])
                        video_url = None
                        
                        for vf in video_files:
                            if vf.get("quality") == "hd" and vf.get("width", 0) >= 1280:
                                video_url = vf.get("link")
                                break
                        
                        if not video_url and video_files:
                            video_url = video_files[0].get("link")
                        
                        if video_url:
                            # Download video
                            clip_filename = os.path.join(clips_folder, f"clip_{len(downloaded_clips)+1}.mp4")
                            
                            vid_response = requests.get(video_url, stream=True, timeout=60)
                            if vid_response.status_code == 200:
                                with open(clip_filename, "wb") as f:
                                    for chunk in vid_response.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                downloaded_clips.append(clip_filename)
                                print(f"  Downloaded clip {len(downloaded_clips)}/{clips_needed}")
                                
            except Exception as e:
                print(f"  Warning: Error downloading from '{term}': {e}")
                continue
        
        self.video_clips = downloaded_clips
        print(f"\n  Total clips downloaded: {len(downloaded_clips)}")
        return downloaded_clips
    
    def generate_search_terms(self):
        """Generate search terms based on trending topic"""
        # Extract keywords from topic
        topic_words = self.trending_topic.lower().split()
        
        # Common video search terms
        base_terms = []
        
        # Add topic-specific terms
        for word in topic_words:
            if len(word) > 3 and word not in ['about', 'that', 'will', 'your', 'with', 'from', 'this', 'what', 'have']:
                base_terms.append(word)
                base_terms.append(f"{word} footage")
        
        # Add generic terms based on niche
        niche_terms = {
            "animals": ["wildlife", "nature", "animals", "ocean", "forest"],
            "space": ["space", "galaxy", "stars", "planets", "universe"],
            "gaming": ["gaming", "video games", "esports", "computer"],
            "science": ["science", "laboratory", "experiment", "technology"],
            "food": ["food", "cooking", "kitchen", "restaurant", "delicious"],
            "sports": ["sports", "athletics", "stadium", "competition"],
            "technology": ["technology", "computer", "digital", "futuristic"],
            "amazing facts": ["amazing", "incredible", "world", "nature", "science"]
        }
        
        # Add niche-specific terms
        for key, terms in niche_terms.items():
            if key in CHANNEL_NICHE.lower():
                base_terms.extend(terms)
                break
        else:
            base_terms.extend(niche_terms["amazing facts"])
        
        # Remove duplicates and return
        return list(dict.fromkeys(base_terms))[:10]
    
    # =========================================
    # STEP 5: VIDEO ASSEMBLY
    # =========================================
    def assemble_video(self):
        """Assemble final video from clips and voiceover"""
        self.print_step(5, "ASSEMBLING FINAL VIDEO...")
        
        if not MOVIEPY_AVAILABLE:
            print("  ERROR: MoviePy not available!")
            return None
        
        if not self.voiceover_file or not os.path.exists(self.voiceover_file):
            print("  ERROR: No voiceover file!")
            return None
        
        if not self.video_clips:
            print("  WARNING: No video clips available!")
            print("  Creating video with static background...")
            return self.create_static_video()
        
        try:
            # Load audio
            audio = AudioFileClip(self.voiceover_file)
            audio_duration = audio.duration
            print(f"  Audio duration: {audio_duration:.1f} seconds")
            
            # Calculate clip duration
            num_clips = len(self.video_clips)
            clip_duration = audio_duration / num_clips
            print(f"  Each clip: {clip_duration:.1f} seconds")
            
            # Process video clips
            processed_clips = []
            for i, clip_path in enumerate(self.video_clips):
                try:
                    clip = VideoFileClip(clip_path)
                    
                    # Adjust clip duration
                    if clip.duration < clip_duration:
                        # Loop short clips
                        clip = clip.loop(duration=clip_duration)
                    else:
                        # Trim long clips
                        clip = clip.subclip(0, min(clip_duration, clip.duration))
                    
                    # Resize to standard resolution
                    clip = clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))
                    
                    processed_clips.append(clip)
                    print(f"  Processed clip {i+1}/{num_clips}")
                    
                except Exception as e:
                    print(f"  Warning: Could not process clip {i+1}: {e}")
                    continue
            
            if not processed_clips:
                print("  ERROR: No clips could be processed!")
                return self.create_static_video()
            
            # Concatenate clips
            final_video = concatenate_videoclips(processed_clips, method="compose")
            
            # Add audio
            final_video = final_video.set_audio(audio)
            
            # Output filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.final_video = os.path.join(self.output_folder, f"video_{timestamp}.mp4")
            
            # Write final video
            print(f"\n  Rendering final video...")
            final_video.write_videofile(
                self.final_video,
                fps=VIDEO_FPS,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                logger=None
            )
            
            # Cleanup
            audio.close()
            for clip in processed_clips:
                clip.close()
            final_video.close()
            
            print(f"  Video saved: {self.final_video}")
            return self.final_video
            
        except Exception as e:
            print(f"  ERROR assembling video: {e}")
            return None
    
    def create_static_video(self):
        """Create video with static background when no clips available"""
        try:
            audio = AudioFileClip(self.voiceover_file)
            
            # Create colored background
            background = ColorClip(
                size=(VIDEO_WIDTH, VIDEO_HEIGHT),
                color=(30, 30, 60),
                duration=audio.duration
            )
            
            # Add text
            try:
                txt_clip = TextClip(
                    self.trending_topic,
                    fontsize=60,
                    color='white',
                    size=(VIDEO_WIDTH - 100, None),
                    method='caption'
                ).set_position('center').set_duration(audio.duration)
                
                final = CompositeVideoClip([background, txt_clip])
            except:
                final = background
            
            final = final.set_audio(audio)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.final_video = os.path.join(self.output_folder, f"video_{timestamp}.mp4")
            
            final.write_videofile(
                self.final_video,
                fps=VIDEO_FPS,
                codec='libx264',
                audio_codec='aac',
                threads=4,
                logger=None
            )
            
            audio.close()
            final.close()
            
            return self.final_video
            
        except Exception as e:
            print(f"  ERROR creating static video: {e}")
            return None
    
    # =========================================
    # STEP 6: THUMBNAIL CREATION
    # =========================================
    def create_thumbnail(self):
        """Create eye-catching thumbnail"""
        self.print_step(6, "CREATING THUMBNAIL...")
        
        if not PILLOW_AVAILABLE:
            print("  WARNING: Pillow not available!")
            return None
        
        try:
            # Create image
            img = Image.new('RGB', (1280, 720))
            draw = ImageDraw.Draw(img)
            
            # Create gradient background
            for y in range(720):
                r = int(255 * (1 - y/720) * 0.8)
                g = int(100 * (y/720))
                b = int(200 * (y/720) + 50)
                draw.line([(0, y), (1280, y)], fill=(r, g, b))
            
            # Add text
            # Try to load a font, fall back to default
            try:
                title_font = ImageFont.truetype("arial.ttf", 80)
                subtitle_font = ImageFont.truetype("arial.ttf", 40)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Create title text (shortened if needed)
            title = self.trending_topic[:40] + "..." if len(self.trending_topic) > 40 else self.trending_topic
            
            # Draw title with shadow
            draw.text((642, 312), title.upper(), font=title_font, fill=(0, 0, 0), anchor="mm")
            draw.text((640, 310), title.upper(), font=title_font, fill=(255, 255, 0), anchor="mm")
            
            # Draw subtitle
            subtitle = f"{NUM_FACTS} AMAZING FACTS!"
            draw.text((640, 420), subtitle, font=subtitle_font, fill=(255, 255, 255), anchor="mm")
            
            # Save thumbnail
            self.thumbnail_file = os.path.join(self.output_folder, "thumbnail.jpg")
            img.save(self.thumbnail_file, quality=95)
            
            print(f"  Thumbnail saved: {self.thumbnail_file}")
            return self.thumbnail_file
            
        except Exception as e:
            print(f"  ERROR creating thumbnail: {e}")
            return None
    
    # =========================================
    # STEP 7: YOUTUBE UPLOAD
    # =========================================
    def get_youtube_service(self):
        """Get authenticated YouTube service"""
        if not YOUTUBE_AVAILABLE:
            return None
        
        SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
        credentials = None
        token_file = os.path.join(os.path.dirname(__file__), "token.pickle")
        client_secrets = os.path.join(os.path.dirname(__file__), YOUTUBE_CLIENT_SECRETS)
        
        # Load existing credentials
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
        
        # Refresh or get new credentials
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if not os.path.exists(client_secrets):
                    print(f"  ERROR: {YOUTUBE_CLIENT_SECRETS} not found!")
                    print("  Please download it from Google Cloud Console")
                    return None
                
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
                credentials = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
        
        return build('youtube', 'v3', credentials=credentials)
    
    def upload_to_youtube(self):
        """Upload video to YouTube"""
        self.print_step(7, "UPLOADING TO YOUTUBE...")
        
        if not self.final_video or not os.path.exists(self.final_video):
            print("  ERROR: No video file to upload!")
            return None
        
        # Generate metadata
        self.generate_metadata()
        
        youtube = self.get_youtube_service()
        if not youtube:
            print("  WARNING: YouTube upload skipped (not configured)")
            print("  To enable: Add client_secrets.json from Google Cloud Console")
            self.save_metadata_for_manual_upload()
            return None
        
        try:
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': self.metadata['title'],
                    'description': self.metadata['description'],
                    'tags': self.metadata['tags'],
                    'categoryId': YOUTUBE_CATEGORY
                },
                'status': {
                    'privacyStatus': YOUTUBE_PRIVACY,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Upload video
            media = MediaFileUpload(
                self.final_video,
                mimetype='video/mp4',
                resumable=True
            )
            
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            print("  Uploading video...")
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"  Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response.get('id')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"\n  VIDEO UPLOADED SUCCESSFULLY!")
            print(f"  URL: {video_url}")
            
            # Upload thumbnail if available
            if self.thumbnail_file and os.path.exists(self.thumbnail_file):
                try:
                    youtube.thumbnails().set(
                        videoId=video_id,
                        media_body=MediaFileUpload(self.thumbnail_file)
                    ).execute()
                    print("  Thumbnail uploaded!")
                except:
                    print("  Note: Thumbnail upload requires channel verification")
            
            # Save upload info
            self.save_upload_log(video_id, video_url)
            
            return video_url
            
        except Exception as e:
            print(f"  ERROR uploading to YouTube: {e}")
            self.save_metadata_for_manual_upload()
            return None
    
    def generate_metadata(self):
        """Generate video metadata"""
        # Create title
        title = self.trending_topic
        if len(title) > 100:
            title = title[:97] + "..."
        
        # Create description
        description = f"""
{self.trending_topic}

In this video, we explore {NUM_FACTS} amazing facts that will blow your mind!

Don't forget to:
- LIKE this video if you learned something new!
- SUBSCRIBE for more amazing content!
- COMMENT your favorite fact below!

#facts #amazing #didyouknow #interesting #education

---
Created with Krwutarth's YouTube Automation System
"""
        
        # Create tags
        tags = list(DEFAULT_TAGS)
        topic_words = self.trending_topic.lower().split()
        for word in topic_words:
            if len(word) > 3 and word not in tags:
                tags.append(word)
        tags = tags[:30]  # YouTube limit
        
        self.metadata = {
            'title': title,
            'description': description.strip(),
            'tags': tags
        }
        
        return self.metadata
    
    def save_metadata_for_manual_upload(self):
        """Save metadata for manual upload if automatic fails"""
        metadata_file = os.path.join(self.output_folder, "upload_metadata.txt")
        
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("YOUTUBE UPLOAD METADATA\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"VIDEO FILE: {self.final_video}\n")
            f.write(f"THUMBNAIL: {self.thumbnail_file}\n\n")
            f.write("TITLE:\n")
            f.write(f"{self.metadata.get('title', self.trending_topic)}\n\n")
            f.write("DESCRIPTION:\n")
            f.write(f"{self.metadata.get('description', '')}\n\n")
            f.write("TAGS:\n")
            f.write(f"{', '.join(self.metadata.get('tags', []))}\n")
        
        print(f"  Metadata saved to: {metadata_file}")
        print("  You can use this for manual upload to YouTube Studio")
    
    def save_upload_log(self, video_id, video_url):
        """Save upload log"""
        log_file = os.path.join(self.output_folder, "upload_log.txt")
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 50}\n")
            f.write(f"Upload: {datetime.datetime.now()}\n")
            f.write(f"Topic: {self.trending_topic}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {video_url}\n")
    
    # =========================================
    # MAIN EXECUTION
    # =========================================
    def run(self):
        """Run the complete automation pipeline"""
        self.print_banner()
        
        start_time = datetime.datetime.now()
        print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Discover trends
        if not self.discover_trends():
            print("\nERROR: Could not find trending topic!")
            return False
        
        # Step 2: Generate script
        if not self.generate_script():
            print("\nERROR: Could not generate script!")
            return False
        
        # Step 3: Generate voiceover
        if not self.generate_voiceover():
            print("\nERROR: Could not generate voiceover!")
            return False
        
        # Step 4: Download video clips
        self.download_video_clips()  # Continue even if no clips
        
        # Step 5: Assemble video
        if not self.assemble_video():
            print("\nERROR: Could not assemble video!")
            return False
        
        # Step 6: Create thumbnail
        self.create_thumbnail()  # Continue even if fails
        
        # Step 7: Upload to YouTube
        self.upload_to_youtube()  # Continue even if fails
        
        # Done!
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 70)
        print("   AUTOMATION COMPLETE!")
        print("=" * 70)
        print(f"\n  Topic: {self.trending_topic}")
        print(f"  Video: {self.final_video}")
        print(f"  Thumbnail: {self.thumbnail_file}")
        print(f"  Duration: {duration:.1f} seconds")
        print("\n  Check the 'output' folder for all files!")
        print("=" * 70 + "\n")
        
        return True


def main():
    """Main entry point"""
    automation = YouTubeAutomation()
    success = automation.run()
    
    if not success:
        print("\nSome steps failed. Check the errors above.")
    
    # Keep window open on Windows
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
