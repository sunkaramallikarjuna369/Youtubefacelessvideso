"""
KRWUTARTH'S COMPLETE AUTOMATION - CONFIGURATION
================================================
Edit these settings to customize your video automation!
"""

# ===========================================
# YOUR CHANNEL NICHE
# ===========================================
# What kind of videos do you want to make?
# Examples: "animals", "space", "gaming", "science", "sports", "food", "technology"
CHANNEL_NICHE = "amazing facts"

# Keywords related to your niche (helps find better trends)
NICHE_KEYWORDS = ["facts", "amazing", "interesting", "cool", "mind blowing", "did you know"]

# ===========================================
# VIDEO SETTINGS
# ===========================================
# How many facts per video?
NUM_FACTS = 5

# Video resolution
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080

# Frames per second
VIDEO_FPS = 30

# ===========================================
# VOICE SETTINGS
# ===========================================
# Voice options:
# - "en-US-GuyNeural" (male, American)
# - "en-US-JennyNeural" (female, American)
# - "en-GB-RyanNeural" (male, British)
# - "en-AU-WilliamNeural" (male, Australian)
VOICE = "en-US-GuyNeural"

# Voice speed (1.0 = normal, 1.1 = slightly faster)
VOICE_SPEED = 1.0

# ===========================================
# API KEYS (REQUIRED)
# ===========================================
# Get your free Pexels API key from: https://www.pexels.com/api/
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"

# YouTube client secrets file (download from Google Cloud Console)
YOUTUBE_CLIENT_SECRETS = "client_secrets.json"

# ===========================================
# OLLAMA SETTINGS (LOCAL AI)
# ===========================================
# Make sure Ollama is running: ollama serve
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"

# ===========================================
# OUTPUT SETTINGS
# ===========================================
OUTPUT_FOLDER = "output"

# ===========================================
# YOUTUBE UPLOAD SETTINGS
# ===========================================
# Privacy: "public", "private", or "unlisted"
YOUTUBE_PRIVACY = "public"

# Category ID (22 = People & Blogs, 24 = Entertainment, 27 = Education, 28 = Science & Technology)
YOUTUBE_CATEGORY = "27"

# Default tags for all videos
DEFAULT_TAGS = ["facts", "amazing facts", "did you know", "interesting", "education"]

# ===========================================
# SCHEDULING SETTINGS
# ===========================================
# How many videos to create per day?
VIDEOS_PER_DAY = 1

# What time to create videos? (24-hour format)
SCHEDULE_HOUR = 10
SCHEDULE_MINUTE = 0

# ===========================================
# TREND DISCOVERY SETTINGS
# ===========================================
# Country for trends (US, GB, IN, etc.)
TREND_COUNTRY = "US"

# How many trending topics to check?
NUM_TRENDS_TO_CHECK = 20
