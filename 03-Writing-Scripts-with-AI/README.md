# Module 3: Writing Scripts with AI Help!

## Hey Krwutarth! Let's Make AI Write for You!

Here's a secret: You don't have to write everything yourself! AI (Artificial Intelligence) can help you write awesome video scripts in minutes. It's like having a super-smart robot friend who loves to write!

## What is a Video Script?

A **script** is what you (or the AI voice) will say in your video. It's like the words in a movie!

**Example script for a 1-minute video:**

```
[INTRO]
Did you know that octopuses have THREE hearts? 
That's right - three! And that's just the beginning.
Today, we're looking at 5 mind-blowing facts about octopuses!

[FACT 1]
Number one: Octopuses have blue blood!
Unlike humans who have red blood, octopuses have blue blood 
because it contains copper instead of iron.

[FACT 2]
Number two: They can taste with their arms!
Each arm has hundreds of suckers, and each sucker can taste!
Imagine tasting your food with your hands!

[OUTRO]
If you enjoyed these facts, smash that subscribe button 
and check out our other videos!
```

## Meet Your AI Writing Helpers!

### Ollama (FREE - Runs on Your Computer!)

Ollama is an AI that lives on YOUR computer. No internet needed after you set it up!

**Why it's awesome:**
- 100% FREE forever
- Works without internet
- Private - no one sees what you write
- Fast!

### How to Use Ollama

**Step 1: Make sure Ollama is running**

Open Command Prompt and type:
```
ollama serve
```

Leave this window open! (It needs to keep running)

**Step 2: Open a NEW Command Prompt window**

**Step 3: Talk to the AI!**

Type this to test it:
```
ollama run llama3.1:8b "Write a fun fact about dogs"
```

The AI will write something for you! Cool, right?

## Your First AI Script!

Let's create a Python script that writes video scripts for you!

### Step 1: Create the Script File

1. Open Notepad
2. Copy and paste this code:

```python
"""
Krwutarth's AI Script Writer!
This program uses AI to write YouTube video scripts for you!
"""

import requests

def write_script(topic, num_points=5):
    """Ask AI to write a script about any topic!"""
    
    print(f"Writing a script about: {topic}")
    print("Please wait... the AI is thinking!")
    print()
    
    # This is what we ask the AI to do
    prompt = f"""Write a fun, engaging YouTube video script about: {topic}

The script should:
- Start with an exciting hook to grab attention
- Have {num_points} main points
- Be written for kids/teenagers
- Sound natural and fun, not boring!
- End with a call to action (subscribe, like, etc.)

Make it about 2 minutes long when read out loud."""

    try:
        # Send the request to Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # Wait up to 2 minutes
        )
        
        # Get the AI's response
        result = response.json()
        script = result.get('response', 'Oops! No response received.')
        
        return script
        
    except requests.exceptions.ConnectionError:
        return "ERROR: Ollama isn't running! Open Command Prompt and type: ollama serve"
    except Exception as e:
        return f"ERROR: Something went wrong - {str(e)}"

# === MAIN PROGRAM ===
if __name__ == "__main__":
    print("=" * 50)
    print("KRWUTARTH'S AI SCRIPT WRITER!")
    print("=" * 50)
    print()
    
    # Change this to whatever topic you want!
    my_topic = "5 Amazing Facts About Sharks"
    
    # Generate the script
    script = write_script(my_topic)
    
    # Show the script
    print("HERE'S YOUR SCRIPT:")
    print("-" * 50)
    print(script)
    print("-" * 50)
    
    # Save it to a file
    with open("my_script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    
    print()
    print("Script saved to: my_script.txt")
    print()
    input("Press Enter to close...")
```

3. Save it as `script_writer.py` in your youtube-videos folder

### Step 2: Run It!

1. Make sure Ollama is running (in another Command Prompt: `ollama serve`)
2. Open Command Prompt in your youtube-videos folder
3. Type: `python script_writer.py`
4. Wait about 30-60 seconds
5. Your script appears!

### Step 3: Customize It!

In the code, find this line:
```python
my_topic = "5 Amazing Facts About Sharks"
```

Change it to whatever YOU want:
```python
my_topic = "10 Coolest Minecraft Building Tips"
```

Or:
```python
my_topic = "Why Dinosaurs Were Awesome"
```

## Script Writing Tips

### The Perfect Script Structure

Every good video script has these parts:

**1. THE HOOK (First 5 seconds)**
Grab attention immediately!
- Ask a surprising question
- Share a shocking fact
- Make a bold statement

**Examples:**
- "What if I told you that you've been tying your shoes wrong your whole life?"
- "This tiny creature can kill you in 3 minutes!"
- "95% of people don't know this Minecraft trick!"

**2. THE INTRO (Next 10-15 seconds)**
Tell them what the video is about.

**Example:**
"Today, we're counting down the 5 most dangerous animals that look totally harmless!"

**3. THE MAIN CONTENT**
Your facts, tips, or story points.

**Tips:**
- Number your points ("Number 1...", "Number 2...")
- Keep each point short (30-60 seconds)
- Add interesting details

**4. THE OUTRO (Last 15-20 seconds)**
End strong and tell them what to do!

**Example:**
"If you enjoyed this video, smash that like button and subscribe for more awesome content! See you in the next one!"

## Making Your Scripts Better

### Add Personality!
Don't be boring! Add:
- Jokes
- Sound effect cues [BOOM!]
- Questions to the viewer
- Excitement!

**Boring:** "Sharks have many teeth."
**Better:** "Get this - sharks can have up to 3,000 teeth at once! That's like having a mouth full of knives!"

### Keep It Simple
You're making videos for regular people, not scientists!

**Too complicated:** "The cephalopod's chromatophores enable rapid pigmentation alterations."
**Better:** "Octopuses can change color in less than a second! How cool is that?"

### Use Short Sentences
People listen to videos - they don't read them. Short sentences are easier to follow!

## Practice: Write Your Own Script!

Try writing a script for this topic: "3 Cool Facts About [Your Favorite Animal]"

Use this template:

```
[HOOK]
(Write something surprising to grab attention)

[INTRO]
Today we're looking at 3 amazing facts about [animal]!

[FACT 1]
First up... (write your fact here)

[FACT 2]
Number two... (write your fact here)

[FACT 3]
And finally... (write your fact here)

[OUTRO]
If you learned something new, hit that subscribe button!
See you in the next video!
```

## Advanced: Different Script Types

### List Videos ("Top 5...", "10 Best...")
- Number each item
- Build up to the best one
- Keep each item similar length

### Story Videos
- Set the scene
- Build tension
- Have a climax
- End with a conclusion

### How-To Videos
- State the goal
- List what's needed
- Step-by-step instructions
- Show the result

### Fact Videos
- Hook with the most interesting fact
- Explain each fact clearly
- Add "why it matters"

## Your Assignment!

Before Module 4:

1. **Run the script_writer.py** program
2. **Generate 3 different scripts** (change the topic each time)
3. **Read them out loud** - do they sound natural?
4. **Save your favorite one** - you'll use it later!

## Key Words to Remember

| Word | What It Means |
|------|---------------|
| Script | The words spoken in your video |
| Hook | The attention-grabbing start |
| Prompt | What you tell the AI to do |
| Outro | The ending of your video |
| Call to Action | Telling viewers to subscribe/like |

## Quick Quiz!

1. What are the 4 parts of a good script?
2. Why is the "hook" important?
3. What does Ollama do?
4. How do you make scripts sound more interesting?

---

## Achievement Unlocked!

**"Script Master"** - You can now create video scripts with AI!

**Progress: Module 3 of 12 Complete!**

Next up: Module 4 - Making Cool Robot Voices! You'll turn your scripts into audio!
