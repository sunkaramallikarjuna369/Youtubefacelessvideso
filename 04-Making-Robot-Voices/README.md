# Module 4: Making Cool Robot Voices!

## Hey Krwutarth! Let's Turn Text into Speech!

Now that you can write scripts, let's turn those words into actual voices! We'll use a tool called **Edge TTS** that makes your computer talk. And the best part? It's 100% FREE with no limits!

## What is Text-to-Speech (TTS)?

**Text-to-Speech** = Your computer reads text out loud!

You type words, and the computer turns them into audio that sounds like a real person talking. It's like magic!

## Meet Edge TTS - Your Free Voice Generator!

Edge TTS uses Microsoft's voices (the same ones in Windows). They sound really natural - not like old robot voices!

**Why Edge TTS is awesome:**
- Completely FREE
- No limits on how much you use it
- Sounds natural and professional
- Works offline after setup
- Many different voices to choose from!

## Available Voices

Here are some cool voices you can use:

### American English Voices
| Voice Name | Type | Good For |
|------------|------|----------|
| en-US-GuyNeural | Male, Adult | Facts, tutorials |
| en-US-JennyNeural | Female, Adult | Stories, explanations |
| en-US-AriaNeural | Female, Young | Fun, energetic content |
| en-US-DavisNeural | Male, Deep | Serious topics |
| en-US-TonyNeural | Male, Friendly | Casual content |

### British English Voices
| Voice Name | Type | Good For |
|------------|------|----------|
| en-GB-RyanNeural | Male | Documentary style |
| en-GB-SoniaNeural | Female | Elegant narration |

### Other Cool Voices
| Voice Name | Type | Good For |
|------------|------|----------|
| en-AU-WilliamNeural | Australian Male | Fun, different |
| en-IN-NeerjaNeural | Indian Female | Educational |

## Your First Voice Generation!

Let's create your first voiceover!

### Step 1: Create the Voice Script

1. Open Notepad
2. Copy and paste this code:

```python
"""
Krwutarth's Voice Generator!
Turn any text into a cool voiceover!
"""

import edge_tts
import asyncio

async def create_voice(text, voice_name, output_file):
    """Turn text into speech and save it as an audio file!"""
    
    print(f"Creating voiceover with voice: {voice_name}")
    print("Please wait...")
    
    # Create the voice
    communicate = edge_tts.Communicate(text, voice_name)
    
    # Save it to a file
    await communicate.save(output_file)
    
    print(f"Done! Saved to: {output_file}")

# === YOUR SCRIPT GOES HERE ===
my_script = """
Hey there, awesome viewers!

Welcome back to another amazing video!

Today, we're going to learn something super cool that will blow your mind.

Did you know that honey never spoils? 
Archaeologists have found 3000 year old honey in Egyptian tombs, 
and it was still perfectly good to eat!

If you enjoyed this fact, smash that subscribe button 
and I'll see you in the next video!

Peace out!
"""

# Choose your voice (try different ones!)
my_voice = "en-US-GuyNeural"

# Output file name
output_file = "my_voiceover.mp3"

# Run the voice generator
asyncio.run(create_voice(my_script, my_voice, output_file))

print()
print("Your voiceover is ready!")
print(f"Look for '{output_file}' in your folder!")
input("Press Enter to close...")
```

3. Save it as `voice_maker.py` in your youtube-videos folder

### Step 2: Run It!

1. Open Command Prompt in your youtube-videos folder
2. Type: `python voice_maker.py`
3. Wait a few seconds
4. Check your folder - you'll have a new `my_voiceover.mp3` file!

### Step 3: Listen to It!

Double-click the MP3 file to play it. You just created your first AI voiceover!

## Try Different Voices!

Change this line in the code:
```python
my_voice = "en-US-GuyNeural"
```

To try other voices:
```python
my_voice = "en-US-JennyNeural"  # Female voice
```
or
```python
my_voice = "en-GB-RyanNeural"  # British male
```
or
```python
my_voice = "en-US-AriaNeural"  # Young female
```

Run the script again and compare the voices!

## Advanced: Voice with Different Speeds and Styles

Want to make the voice faster, slower, or different? Here's an advanced version:

```python
"""
Krwutarth's Advanced Voice Generator!
Control speed, pitch, and more!
"""

import edge_tts
import asyncio

async def create_advanced_voice(text, voice_name, output_file, rate="+0%", pitch="+0Hz"):
    """
    Create a voiceover with custom settings!
    
    rate: Speed of speech
        "+50%" = 50% faster
        "-25%" = 25% slower
        "+0%" = normal speed
    
    pitch: How high or low the voice sounds
        "+10Hz" = slightly higher
        "-10Hz" = slightly lower
        "+0Hz" = normal pitch
    """
    
    print(f"Creating voiceover...")
    print(f"Voice: {voice_name}")
    print(f"Speed: {rate}")
    print(f"Pitch: {pitch}")
    
    # Create the voice with custom settings
    communicate = edge_tts.Communicate(
        text, 
        voice_name,
        rate=rate,
        pitch=pitch
    )
    
    await communicate.save(output_file)
    print(f"Saved to: {output_file}")

# === YOUR SCRIPT ===
my_script = """
Welcome to another epic video!

Today we're counting down the top 5 coolest animals in the ocean!

Number 5: The Mantis Shrimp!
This little guy can punch so fast, it creates a shockwave!

Number 4: The Mimic Octopus!
It can disguise itself as over 15 different animals!

Number 3: The Box Jellyfish!
One of the most venomous creatures on Earth!

Number 2: The Blue Whale!
The largest animal that has EVER existed!

And Number 1: The Great White Shark!
The ultimate ocean predator!

Thanks for watching! Subscribe for more awesome content!
"""

# Settings
voice = "en-US-GuyNeural"
speed = "+10%"  # Slightly faster (try +20% or -10%)
pitch = "+0Hz"  # Normal pitch (try +5Hz for higher)

# Create the voiceover
asyncio.run(create_advanced_voice(
    my_script, 
    voice, 
    "advanced_voiceover.mp3",
    rate=speed,
    pitch=pitch
))

print()
print("Done! Check 'advanced_voiceover.mp3'")
input("Press Enter to close...")
```

## Voice Tips for Better Videos

### 1. Add Pauses
Use `...` or line breaks for natural pauses:
```
"This is amazing... wait for it... BOOM!"
```

### 2. Break Up Long Sentences
Short sentences sound better:
```
Bad: "The blue whale is the largest animal that has ever existed on Earth and it can grow up to 100 feet long and weigh as much as 200 tons."

Good: "The blue whale is the largest animal ever. It can grow up to 100 feet long. That's as long as three school buses!"
```

### 3. Use Numbers Carefully
Write numbers as words for better pronunciation:
```
Bad: "It weighs 200 tons"
Good: "It weighs two hundred tons"
```

### 4. Test Different Voices
Some voices work better for certain content:
- **Guy/Davis** - Good for facts, serious topics
- **Jenny/Aria** - Good for friendly, casual content
- **Ryan (British)** - Good for documentary style

## Batch Voice Generator

Want to create multiple voiceovers at once? Here's a script for that:

```python
"""
Krwutarth's Batch Voice Generator!
Create multiple voiceovers at once!
"""

import edge_tts
import asyncio
import os

async def create_voice(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    print(f"Created: {filename}")

async def batch_create():
    # List of scripts to convert
    scripts = [
        {
            "text": "Welcome to my channel! Subscribe for awesome content!",
            "voice": "en-US-GuyNeural",
            "file": "intro.mp3"
        },
        {
            "text": "Thanks for watching! See you in the next video!",
            "voice": "en-US-GuyNeural", 
            "file": "outro.mp3"
        },
        {
            "text": "Don't forget to like and subscribe!",
            "voice": "en-US-JennyNeural",
            "file": "reminder.mp3"
        }
    ]
    
    print("Creating multiple voiceovers...")
    print()
    
    for script in scripts:
        await create_voice(
            script["text"],
            script["voice"],
            script["file"]
        )
    
    print()
    print("All done!")

# Run it
asyncio.run(batch_create())
input("Press Enter to close...")
```

## List All Available Voices

Want to see ALL available voices? Run this:

```python
"""
List all available Edge TTS voices!
"""

import edge_tts
import asyncio

async def list_voices():
    voices = await edge_tts.list_voices()
    
    print("AVAILABLE VOICES:")
    print("=" * 60)
    
    # Filter for English voices
    english_voices = [v for v in voices if v["Locale"].startswith("en-")]
    
    for voice in english_voices:
        print(f"Name: {voice['ShortName']}")
        print(f"  Gender: {voice['Gender']}")
        print(f"  Locale: {voice['Locale']}")
        print()

asyncio.run(list_voices())
input("Press Enter to close...")
```

## Your Assignment!

Before Module 5:

1. **Create 3 different voiceovers** using different voices
2. **Try changing the speed** (faster and slower)
3. **Create an intro and outro** for your future videos
4. **Pick your favorite voice** for your channel

## Key Words to Remember

| Word | What It Means |
|------|---------------|
| TTS | Text-to-Speech - computer reads text aloud |
| Voice | The specific speaker style |
| Rate | How fast the voice speaks |
| Pitch | How high or low the voice sounds |
| MP3 | Audio file format |

## Quick Quiz!

1. What does TTS stand for?
2. Name 3 different voices you can use
3. How do you make the voice speak faster?
4. Why should you use short sentences in scripts?

---

## Achievement Unlocked!

**"Voice Wizard"** - You can now create AI voiceovers!

**Progress: Module 4 of 12 Complete!**

Next up: Module 5 - Finding Cool Videos & Pictures! You'll learn where to get free visuals for your videos!
