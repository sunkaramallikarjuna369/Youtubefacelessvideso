# Module 7: Setting Up Your YouTube Channel!

## Hey Krwutarth! Time to Create Your Channel!

You've learned how to make videos - now let's create your YouTube channel so the world can see your awesome content!

## Before You Start - Important for Kids!

Since you're 12, you'll need a parent's help for some things:
- Creating a Google account (if you don't have one)
- Setting up monetization later
- Managing any money you earn

**Ask your parent to help you with the account setup!**

## Step 1: Create a Google Account

If you don't have a Google account:

1. Go to: https://accounts.google.com
2. Click "Create account"
3. Choose "For myself"
4. Fill in your information
5. **Important:** Use your parent's email for recovery!

## Step 2: Create Your YouTube Channel

1. Go to: https://www.youtube.com
2. Sign in with your Google account
3. Click on your profile picture (top right)
4. Click "Create a channel"
5. Choose "Use a custom name" (recommended!)
6. Enter your channel name

### Choosing a Channel Name

Your channel name is SUPER important! Here are some tips:

**Good channel names:**
- Easy to remember
- Related to your content
- Unique and catchy
- Easy to spell

**Examples:**
- "Krwutarth's Cool Facts"
- "Epic Gaming Tips"
- "Mind Blown Facts"
- "The Fact Factory"

**Avoid:**
- Hard to spell names
- Numbers that look like letters (like "F4ct5")
- Names too similar to big channels
- Super long names

## Step 3: Customize Your Channel

### Add a Profile Picture

Your profile picture shows up everywhere! Make it:
- Simple and recognizable
- Related to your content
- Clear even when small

**Free tools to create one:**
- Canva (canva.com) - FREE!
- GIMP - FREE software

**Size:** 800 x 800 pixels

### Add a Banner Image

The banner is the big image at the top of your channel.

**Size:** 2560 x 1440 pixels (but most shows as 1546 x 423)

**What to include:**
- Your channel name
- What your channel is about
- Upload schedule (like "New videos every week!")

### Create a Banner with Python!

Here's a script to create a simple banner:

```python
"""
Krwutarth's Banner Creator!
Create a YouTube channel banner!
"""

from PIL import Image, ImageDraw, ImageFont

def create_banner(channel_name, tagline, output_file):
    """Create a YouTube channel banner"""
    
    # Banner size
    width = 2560
    height = 1440
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create gradient (dark blue to purple)
    for y in range(height):
        # Calculate color for this row
        r = int(20 + (y / height) * 60)
        g = int(20 + (y / height) * 20)
        b = int(80 + (y / height) * 100)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add channel name (big text in center)
    try:
        # Try to use a nice font
        title_font = ImageFont.truetype("arial.ttf", 150)
        tagline_font = ImageFont.truetype("arial.ttf", 60)
    except:
        # Use default font if arial not found
        title_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
    
    # Draw channel name
    title_bbox = draw.textbbox((0, 0), channel_name, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = height // 2 - 100
    
    # Add shadow effect
    draw.text((title_x + 4, title_y + 4), channel_name, font=title_font, fill=(0, 0, 0))
    draw.text((title_x, title_y), channel_name, font=title_font, fill=(255, 255, 255))
    
    # Draw tagline
    tag_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tag_width = tag_bbox[2] - tag_bbox[0]
    tag_x = (width - tag_width) // 2
    tag_y = title_y + 180
    
    draw.text((tag_x, tag_y), tagline, font=tagline_font, fill=(200, 200, 255))
    
    # Save the banner
    img.save(output_file)
    print(f"Banner saved to: {output_file}")

# Create your banner!
create_banner(
    channel_name="KRWUTARTH'S FACTS",
    tagline="Amazing Facts Every Week!",
    output_file="my_channel_banner.png"
)

print("Done! Upload this to your YouTube channel!")
input("Press Enter to close...")
```

## Step 4: Write Your Channel Description

Your description tells people what your channel is about.

**Template:**

```
Welcome to [Channel Name]! 🎬

Here you'll find [what kind of videos you make].

New videos every [your schedule]!

What you'll learn:
• [Topic 1]
• [Topic 2]
• [Topic 3]

Subscribe and hit the bell to never miss a video!

For business inquiries: [parent's email]
```

**Example:**

```
Welcome to Krwutarth's Cool Facts! 🎬

Here you'll find amazing facts about animals, space, science, and more!

New videos every Saturday!

What you'll discover:
• Mind-blowing animal facts
• Space mysteries explained
• Science made fun and easy

Subscribe and hit the bell to never miss a video!

For business inquiries: parent@email.com
```

## Step 5: Channel Settings

### Important Settings to Check:

1. **Go to YouTube Studio** (studio.youtube.com)
2. Click **Settings** (bottom left)
3. Check these:

**Channel > Basic info:**
- Add keywords related to your content
- Set your country

**Upload defaults:**
- Set default title format
- Set default description template
- Set default tags

**Permissions:**
- Keep this secure!

## Step 6: Create Your First Playlist

Playlists organize your videos and help viewers find more content!

1. Go to your channel
2. Click "Playlists"
3. Click "New playlist"
4. Name it (like "Animal Facts" or "Gaming Tips")
5. Add a description

## Channel Branding Checklist

Before uploading your first video, make sure you have:

- [ ] Channel name chosen
- [ ] Profile picture uploaded
- [ ] Banner image uploaded
- [ ] Channel description written
- [ ] At least one playlist created
- [ ] Channel keywords added

## Tips for a Professional-Looking Channel

### 1. Be Consistent
Use the same colors and style everywhere!

### 2. Fill Out Everything
Empty sections look unprofessional.

### 3. Use High-Quality Images
Blurry images = unprofessional look.

### 4. Keep It Simple
Don't overcomplicate your branding.

### 5. Make It Memorable
People should remember your channel!

## Your Assignment!

Before Module 8:

1. **Create your YouTube channel** (with parent help!)
2. **Choose a channel name**
3. **Create and upload a profile picture**
4. **Create and upload a banner**
5. **Write your channel description**
6. **Create at least one playlist**

## Key Words to Remember

| Word | What It Means |
|------|---------------|
| Channel | Your YouTube page where all your videos live |
| Banner | The big image at the top of your channel |
| Profile Picture | The small image that represents you |
| Playlist | A collection of videos grouped together |
| Branding | Your channel's look and feel |

## Quick Quiz!

1. What size should your profile picture be?
2. Why is your channel name important?
3. What should you include in your channel description?
4. Why are playlists useful?

---

## Achievement Unlocked!

**"Channel Creator"** - You have your own YouTube channel!

**Progress: Module 7 of 12 Complete!**

Next up: Module 8 - Getting People to Watch (SEO)! Learn how to get more views!
