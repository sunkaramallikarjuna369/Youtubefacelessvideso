# Complete YouTube Video Automation System

## Hey Krwutarth! This is the ULTIMATE Automation!

This script does EVERYTHING automatically with ZERO manual intervention:
1. Finds trending topics on the internet
2. Picks the best topic for your channel
3. Writes a video script using AI (Ollama - runs locally)
4. Creates a voiceover (Edge TTS - 100% free)
5. Downloads video clips (Pexels - free)
6. Assembles the final video
7. Creates a thumbnail
8. Uploads to YouTube automatically!

## Quick Start (Windows)

### Step 1: One-Time Setup
1. Double-click `INSTALL_REQUIREMENTS.bat` to install all packages
2. Make sure Ollama is installed and running (`ollama serve`)
3. Get a free Pexels API key from https://www.pexels.com/api/
4. Edit `config.py` and add your Pexels API key

### Step 2: Run Automation
- **Option A**: Double-click `RUN_AUTOMATION.bat` to create one video
- **Option B**: Double-click `RUN_SCHEDULER.bat` to run daily automation

That's it! The script handles everything else automatically!

## Files Included

| File | What It Does |
|------|--------------|
| `RUN_AUTOMATION.bat` | Double-click to create one video |
| `RUN_SCHEDULER.bat` | Double-click to start daily automation |
| `INSTALL_REQUIREMENTS.bat` | Double-click to install packages |
| `auto_video_creator.py` | Main automation script |
| `scheduler.py` | Daily scheduler script |
| `config.py` | Your settings (edit this!) |

## Setup Details

### Required: Ollama (Local AI)
1. Download from https://ollama.ai
2. Install it
3. Open Command Prompt and run: `ollama pull llama3.1:8b`
4. Keep Ollama running: `ollama serve`

### Required: Pexels API Key (Free)
1. Go to https://www.pexels.com/api/
2. Sign up for free
3. Copy your API key
4. Paste it in `config.py` where it says `YOUR_PEXELS_API_KEY_HERE`

### Optional: YouTube Auto-Upload
To enable automatic YouTube uploads:
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `client_secrets.json`
6. Put it in this folder

If you skip this, videos will be saved locally and you can upload manually.

## 100% Free Tools Used

| Tool | Purpose | Cost |
|------|---------|------|
| Ollama | AI script writing | FREE (runs locally) |
| Edge TTS | Voice generation | FREE (unlimited) |
| Pexels | Video clips | FREE (with API key) |
| MoviePy | Video editing | FREE |
| Pillow | Thumbnails | FREE |
| YouTube API | Uploading | FREE |

## Troubleshooting

**"Ollama not running"**
- Open Command Prompt
- Run: `ollama serve`
- Keep it running while using automation

**"No Pexels API key"**
- Get free key from https://www.pexels.com/api/
- Add it to `config.py`

**"YouTube upload failed"**
- Videos are saved in `output` folder
- Upload manually to YouTube Studio
- Or set up YouTube API (see setup above)

---

**Achievement Unlocked: Full Automation Master!**

Now Krwutarth can create YouTube videos automatically every day!
