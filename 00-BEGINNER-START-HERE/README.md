# Complete Beginner's Guide - Start Here!

Welcome! This guide will help you set up everything from scratch, even if you've never written code before. Follow each step carefully, and you'll be creating automated faceless YouTube videos in no time.

## What You'll Learn

By the end of this setup, you'll have:
- Python installed and working
- All necessary tools ready to use
- Your first test script running successfully
- Everything needed to start creating videos

## Step 1: Install Python

Python is the programming language we'll use for automation. Don't worry - you don't need to learn programming! You'll just copy and run the scripts provided.

### For Windows Users

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Click the big yellow "Download Python 3.x.x" button
   - Save the file to your Downloads folder

2. **Install Python**
   - Double-click the downloaded file
   - **IMPORTANT**: Check the box that says "Add Python to PATH" at the bottom!
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation**
   - Press `Windows Key + R`
   - Type `cmd` and press Enter
   - In the black window, type: `python --version`
   - You should see something like: `Python 3.11.5`

### For Mac Users

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Click the big yellow "Download Python 3.x.x" button
   - Save and open the downloaded .pkg file

2. **Install Python**
   - Follow the installer prompts
   - Click "Continue" and "Agree" as needed
   - Click "Install"
   - Enter your Mac password if asked

3. **Verify Installation**
   - Press `Cmd + Space`
   - Type `Terminal` and press Enter
   - In the terminal, type: `python3 --version`
   - You should see something like: `Python 3.11.5`

### For Linux Users

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

---

## Step 2: Create Your Project Folder

Let's create a dedicated folder for all your YouTube automation work.

### Windows
1. Open File Explorer
2. Go to your Documents folder
3. Right-click → New → Folder
4. Name it: `youtube-automation`

### Mac/Linux
```bash
mkdir ~/Documents/youtube-automation
cd ~/Documents/youtube-automation
```

---

## Step 3: Open Command Line in Your Project Folder

### Windows
1. Open File Explorer
2. Navigate to your `youtube-automation` folder
3. Click in the address bar at the top
4. Type `cmd` and press Enter
5. A black command window will open in that folder

### Mac
1. Open Finder
2. Navigate to your `youtube-automation` folder
3. Right-click the folder
4. Select "New Terminal at Folder"

### Linux
```bash
cd ~/Documents/youtube-automation
```

---

## Step 4: Install Required Tools

Copy and paste these commands one at a time into your command line. Press Enter after each one.

### Essential Tools (Required)

```bash
# Install Edge TTS (Free voice generation)
pip install edge-tts

# Install video processing tools
pip install moviepy

# Install image processing
pip install Pillow

# Install for downloading stock footage
pip install requests

# Install for environment variables
pip install python-dotenv
```

### Optional Tools (Install Later If Needed)

```bash
# For Google Gemini AI (free tier)
pip install google-generativeai

# For advanced video editing
pip install opencv-python

# For YouTube uploads
pip install google-auth-oauthlib google-api-python-client
```

---

## Step 5: Install Ollama (Free AI for Scripts)

Ollama lets you run AI on your computer for free - no internet needed after setup!

### Windows
1. Go to: https://ollama.com/download
2. Click "Download for Windows"
3. Run the installer
4. Follow the prompts

### Mac
```bash
# Open Terminal and run:
brew install ollama

# If you don't have Homebrew, first install it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Download an AI Model

After installing Ollama, run this command:

```bash
ollama pull llama3.1:8b
```

This downloads a powerful AI model (about 4GB). Wait for it to complete.

---

## Step 6: Get Your Free API Keys

### Pexels API (Free Stock Footage)

1. Go to: https://www.pexels.com/api/
2. Click "Get Started" or "Join"
3. Create a free account (use your email)
4. After logging in, you'll see your API key
5. Copy and save it somewhere safe

### Pixabay API (More Free Stock Footage)

1. Go to: https://pixabay.com/api/docs/
2. Click "Join" to create account
3. After logging in, your API key is shown on the page
4. Copy and save it

### Google Gemini API (Free AI - Optional)

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and save it

---

## Step 7: Create Your Configuration File

Create a file to store your API keys safely.

### Windows
1. Open Notepad
2. Copy and paste this:

```
PEXELS_API_KEY=paste_your_pexels_key_here
PIXABAY_API_KEY=paste_your_pixabay_key_here
GEMINI_API_KEY=paste_your_gemini_key_here
```

3. Replace the placeholder text with your actual keys
4. Click File → Save As
5. Navigate to your `youtube-automation` folder
6. In "File name" type: `.env` (including the dot!)
7. In "Save as type" select: "All Files"
8. Click Save

### Mac/Linux
```bash
cd ~/Documents/youtube-automation

# Create the file
nano .env
```

Paste this content:
```
PEXELS_API_KEY=paste_your_pexels_key_here
PIXABAY_API_KEY=paste_your_pixabay_key_here
GEMINI_API_KEY=paste_your_gemini_key_here
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

---

## Step 8: Test Your Setup

Let's make sure everything works! Create a test file.

### Create Test File

1. Open a text editor (Notepad on Windows, TextEdit on Mac)
2. Copy and paste this entire code:

```python
#!/usr/bin/env python3
"""
Setup Test Script
Run this to verify everything is installed correctly
"""

import sys

print("=" * 50)
print("FACELESS YOUTUBE AUTOMATION - SETUP TEST")
print("=" * 50)
print()

# Test 1: Python Version
print("TEST 1: Python Version")
print(f"  Python {sys.version}")
if sys.version_info >= (3, 8):
    print("  [PASS] Python version is good!")
else:
    print("  [FAIL] Please install Python 3.8 or higher")
print()

# Test 2: Edge TTS
print("TEST 2: Edge TTS (Voice Generation)")
try:
    import edge_tts
    print("  [PASS] Edge TTS is installed!")
except ImportError:
    print("  [FAIL] Run: pip install edge-tts")
print()

# Test 3: MoviePy
print("TEST 3: MoviePy (Video Processing)")
try:
    import moviepy
    print("  [PASS] MoviePy is installed!")
except ImportError:
    print("  [FAIL] Run: pip install moviepy")
print()

# Test 4: Pillow
print("TEST 4: Pillow (Image Processing)")
try:
    from PIL import Image
    print("  [PASS] Pillow is installed!")
except ImportError:
    print("  [FAIL] Run: pip install Pillow")
print()

# Test 5: Requests
print("TEST 5: Requests (API Calls)")
try:
    import requests
    print("  [PASS] Requests is installed!")
except ImportError:
    print("  [FAIL] Run: pip install requests")
print()

# Test 6: Environment File
print("TEST 6: Environment Configuration")
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    pexels = os.getenv('PEXELS_API_KEY')
    if pexels and pexels != 'paste_your_pexels_key_here':
        print("  [PASS] Pexels API key configured!")
    else:
        print("  [WARN] Pexels API key not set (optional)")
except ImportError:
    print("  [FAIL] Run: pip install python-dotenv")
print()

# Test 7: Ollama
print("TEST 7: Ollama (Local AI)")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        models = response.json().get('models', [])
        if models:
            print(f"  [PASS] Ollama running with {len(models)} model(s)!")
        else:
            print("  [WARN] Ollama running but no models. Run: ollama pull llama3.1:8b")
    else:
        print("  [WARN] Ollama not responding. Start it with: ollama serve")
except:
    print("  [WARN] Ollama not running. Start it with: ollama serve")
print()

print("=" * 50)
print("SETUP TEST COMPLETE!")
print("=" * 50)
print()
print("If you see any [FAIL] messages, follow the instructions to fix them.")
print("If you see [WARN] messages, those are optional but recommended.")
print()
input("Press Enter to close...")
```

3. Save the file as `test_setup.py` in your `youtube-automation` folder

### Run the Test

**Windows:**
1. Open Command Prompt in your youtube-automation folder
2. Type: `python test_setup.py`
3. Press Enter

**Mac/Linux:**
```bash
cd ~/Documents/youtube-automation
python3 test_setup.py
```

You should see [PASS] for most tests. Fix any [FAIL] items before continuing.

---

## Step 9: Your First Voice Generation Test

Let's create your first AI voiceover!

### Create the Script

1. Create a new file called `my_first_voice.py`
2. Copy and paste this code:

```python
#!/usr/bin/env python3
"""
My First Voice Generation
Creates a sample voiceover using Edge TTS (100% free!)
"""

import edge_tts
import asyncio

async def create_voiceover():
    # The text to convert to speech
    text = """
    Welcome to my channel! 
    In today's video, we're going to explore something amazing.
    Make sure to subscribe and hit the notification bell 
    so you don't miss any future content.
    Let's get started!
    """
    
    # Choose a voice (try different ones!)
    # Options: en-US-GuyNeural, en-US-JennyNeural, en-GB-RyanNeural
    voice = "en-US-GuyNeural"
    
    # Create the voiceover
    print("Creating voiceover...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("my_first_voiceover.mp3")
    print("Done! Check 'my_first_voiceover.mp3' in your folder!")

# Run the script
asyncio.run(create_voiceover())
```

3. Save the file

### Run It

**Windows:**
```bash
python my_first_voice.py
```

**Mac/Linux:**
```bash
python3 my_first_voice.py
```

Check your folder - you should have a new `my_first_voiceover.mp3` file! Play it to hear your AI voiceover.

---

## Step 10: Your First AI Script Generation

Let's use Ollama to write a video script!

### Make Sure Ollama is Running

**Windows:** Open a new Command Prompt and type:
```bash
ollama serve
```

**Mac/Linux:**
```bash
ollama serve &
```

### Create the Script Generator

1. Create a new file called `my_first_script.py`
2. Copy and paste:

```python
#!/usr/bin/env python3
"""
My First AI Script Generator
Uses Ollama (free, local AI) to write video scripts
"""

import requests

def generate_script(topic):
    """Generate a YouTube script using Ollama"""
    
    print(f"Generating script about: {topic}")
    print("Please wait... (this may take 30-60 seconds)")
    print()
    
    prompt = f"""Write a short YouTube video script (about 2 minutes) about: {topic}

Include:
- An attention-grabbing hook at the start
- 3 main points
- A call to action at the end

Make it conversational and engaging."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        result = response.json()
        script = result.get('response', 'No response received')
        
        return script
        
    except requests.exceptions.ConnectionError:
        return "ERROR: Ollama is not running. Please start it with: ollama serve"
    except Exception as e:
        return f"ERROR: {str(e)}"

# Main program
if __name__ == "__main__":
    print("=" * 50)
    print("AI SCRIPT GENERATOR")
    print("=" * 50)
    print()
    
    # You can change this topic to anything you want!
    topic = "5 Simple Habits That Will Change Your Life"
    
    script = generate_script(topic)
    
    print("GENERATED SCRIPT:")
    print("-" * 50)
    print(script)
    print("-" * 50)
    
    # Save to file
    with open("generated_script.txt", "w") as f:
        f.write(script)
    
    print()
    print("Script saved to: generated_script.txt")
    print()
    input("Press Enter to close...")
```

3. Save the file

### Run It

```bash
python my_first_script.py
```

Wait about 30-60 seconds, and you'll have an AI-generated script!

---

## Troubleshooting Common Problems

### "python is not recognized"
- **Windows**: Reinstall Python and make sure to check "Add Python to PATH"
- **Mac/Linux**: Use `python3` instead of `python`

### "pip is not recognized"
- **Windows**: Try `python -m pip install package_name`
- **Mac/Linux**: Try `pip3 install package_name`

### "ModuleNotFoundError: No module named 'xyz'"
Run: `pip install xyz` (replace xyz with the module name)

### "Ollama connection refused"
Make sure Ollama is running:
```bash
ollama serve
```

### "API key not working"
- Make sure you copied the entire key
- Check there are no extra spaces
- Verify the .env file is in the right folder

### Scripts run but nothing happens
- Check for error messages in red
- Make sure you're in the correct folder
- Try running with `python -u script.py` to see output immediately

---

## What's Next?

Congratulations! You've completed the setup. Now you can:

1. **Go to Module 1**: Learn about faceless YouTube channels
2. **Go to Module 9**: Use the complete automation pipeline
3. **Explore each module**: Build your knowledge step by step

Remember: You don't need to understand the code - just copy, paste, and run!

---

## Quick Reference Commands

Keep these handy:

```bash
# Install a Python package
pip install package_name

# Run a Python script
python script_name.py

# Start Ollama
ollama serve

# Download an AI model
ollama pull model_name

# Check Python version
python --version

# List installed packages
pip list
```

---

## Need Help?

If you're stuck:
1. Read the error message carefully
2. Check the Troubleshooting section above
3. Search the error message on Google
4. The error usually tells you exactly what's wrong!

You've got this! Let's start creating amazing faceless YouTube videos!
