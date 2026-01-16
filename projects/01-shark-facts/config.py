"""
Krwutarth's Shark Facts Video - Configuration

Change these settings to customize your video!
"""

# === VIDEO TOPIC ===
# What shark topic do you want to make a video about?
TOPIC = "5 Amazing Facts About Sharks That Will Blow Your Mind"

# How many facts should the video have?
NUM_FACTS = 5

# === VOICE SETTINGS ===
# Which voice should read your script?
# Options: "en-US-GuyNeural" (boy), "en-US-JennyNeural" (girl), "en-GB-RyanNeural" (British)
VOICE = "en-US-GuyNeural"

# How fast should the voice speak? (1.0 = normal, 1.2 = faster, 0.8 = slower)
VOICE_SPEED = 1.0

# === VIDEO SETTINGS ===
# What keywords to search for video clips?
VIDEO_SEARCH_TERMS = ["shark underwater", "shark swimming", "ocean shark", "great white shark"]

# How many video clips to download?
NUM_VIDEO_CLIPS = 5

# === API KEYS ===
# Get your free API key from: https://www.pexels.com/api/
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"

# === OUTPUT SETTINGS ===
# Where to save the finished video
OUTPUT_FOLDER = "output"

# What to name the video file
OUTPUT_FILENAME = "shark_facts_video.mp4"
