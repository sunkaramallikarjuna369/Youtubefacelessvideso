# YouTube Faceless Video Generator - Automation Guide

Complete one-click automation for generating faceless YouTube videos. Just double-click the batch file and your video will be generated automatically!

## Quick Start (Windows)

1. **Double-click `GENERATE_VIDEO.bat`** - This will:
   - Create a virtual environment automatically
   - Install all required dependencies
   - Guide you through API key setup (first time only)
   - Show you a menu to generate videos

2. **First-time setup**: Edit the `.env` file with your API keys when prompted

3. **Generate your first video**: Choose option 1 or 4 from the menu

## Quick Start (Linux/Mac)

```bash
chmod +x generate_video.sh
./generate_video.sh
```

## API Keys Required

Get your FREE API keys from these sources:

| API | Purpose | Get Key From | CPM Impact |
|-----|---------|--------------|------------|
| Groq | AI Script Generation (Fastest) | https://console.groq.com/keys | High quality scripts |
| Gemini | AI Script Generation | https://makersuite.google.com/app/apikey | High quality scripts |
| Pexels | Stock Video Footage | https://www.pexels.com/api/ | Professional footage |
| Pixabay | Additional Stock Footage | https://pixabay.com/api/docs/ | More footage options |

## Command Line Usage

### Basic Usage
```bash
python scripts/master_automation.py --topic "Your Video Topic" --length 8
```

### All Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--topic` | `-t` | Video topic (required unless using --interactive or --suggest-topics) | - |
| `--length` | `-l` | Video length in minutes | 8 |
| `--keywords` | `-k` | Keywords for stock footage search (space-separated) | Auto from topic |
| `--project` | `-p` | Project name for output folder | Auto-generated |
| `--ai` | - | AI provider: auto, groq, gemini, ollama | auto |
| `--suggest-topics` | - | Show trending topics with monetization focus | - |
| `--interactive` | `-i` | Run in interactive mode with prompts | - |

### Examples

```bash
# Generate a video about AI tools
python scripts/master_automation.py --topic "5 AI Tools for Productivity" --length 8

# Use Groq specifically for faster generation
python scripts/master_automation.py -t "Investment Tips for Beginners" -l 10 --ai groq

# See trending topics for better monetization
python scripts/master_automation.py --suggest-topics

# Interactive mode (step-by-step prompts)
python scripts/master_automation.py --interactive

# Custom keywords for footage
python scripts/master_automation.py -t "Space Facts" -k space galaxy stars planets
```

## High CPM Niches (Better Monetization)

Choose topics from these niches for higher ad revenue:

| Niche | CPM Range | Example Topics |
|-------|-----------|----------------|
| **Finance** | $15-$50 | Investment tips, passive income, budgeting |
| **Business** | $12-$35 | Entrepreneurship, marketing, side hustles |
| **Technology** | $10-$30 | AI tools, gadgets, coding tips |
| **Health** | $10-$25 | Fitness, nutrition, mental health |
| **Education** | $8-$20 | Study tips, career advice, skills |

## Output Files

After generation, your files will be in `scripts/projects/video_YYYYMMDD_HHMMSS/`:

```
video_20240115_143022/
├── scripts/
│   └── script.txt          # Generated video script
├── voiceovers/
│   └── voiceover.mp3       # AI-generated voiceover
├── footage/
│   ├── pexels_*.mp4        # Downloaded stock footage
│   └── pixabay_*.mp4       # Additional footage
├── thumbnails/
│   └── thumbnail.png       # Auto-generated thumbnail
├── output/
│   └── final_video.mp4     # Your finished video!
└── metadata/
    └── metadata.json       # Title, description, tags
```

## AI Providers

The script supports multiple AI providers for script generation:

| Provider | Speed | Quality | Requires |
|----------|-------|---------|----------|
| **Groq** | Fastest | Excellent | GROQ_API_KEY |
| **Gemini** | Fast | Excellent | GEMINI_API_KEY |
| **Ollama** | Slow | Good | Local Ollama running |

With `--ai auto` (default), the script tries Groq first, then Gemini, then Ollama.

## Voice Options

The default voice is `en-US-GuyNeural`. You can change it in the script:

| Voice | Description |
|-------|-------------|
| `en-US-GuyNeural` | Male, American (default) |
| `en-US-JennyNeural` | Female, American |
| `en-GB-RyanNeural` | Male, British |
| `en-AU-WilliamNeural` | Male, Australian |

## Troubleshooting

### "No module named 'groq'"
Run: `pip install groq`

### "No PEXELS_API_KEY found"
Edit your `.env` file and add your Pexels API key

### "Could not generate script"
Make sure at least one AI provider is configured:
- Set GROQ_API_KEY in .env, OR
- Set GEMINI_API_KEY in .env, OR
- Run Ollama locally (`ollama serve`)

### Video has no footage
Make sure PEXELS_API_KEY or PIXABAY_API_KEY is set in your `.env` file

### FFmpeg errors
Install FFmpeg: https://ffmpeg.org/download.html

## Tips for Better Videos

1. **Choose high CPM topics** - Finance and business topics earn more
2. **Use specific keywords** - Better keywords = better stock footage
3. **Keep videos 8-10 minutes** - Optimal for YouTube monetization
4. **Add timestamps** - Edit metadata.json after generation
5. **Create custom thumbnails** - The auto-generated ones are basic

## File Structure

```
Youtubefacelessvideso/
├── GENERATE_VIDEO.bat      # Windows one-click launcher
├── generate_video.sh       # Linux/Mac one-click launcher
├── requirements.txt        # Python dependencies
├── .env                    # Your API keys (create from .env.example)
├── .env.example            # API keys template
└── scripts/
    ├── master_automation.py # Main automation script
    └── projects/            # Generated videos go here
```

## Support

If you have issues:
1. Check the troubleshooting section above
2. Make sure all API keys are set correctly
3. Ensure Python 3.8+ is installed
4. Check that FFmpeg is installed for video processing
