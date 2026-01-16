# Module 7: YouTube Channel Setup

## Overview

Setting up your YouTube channel correctly from the start is crucial for growth and monetization. This module covers everything from creating your channel to optimizing it for success.

## Step 1: Create Your YouTube Channel

### Creating a Brand Account (Recommended)

A Brand Account lets you manage your channel separately from your personal Google account and allows multiple managers.

1. Go to https://www.youtube.com
2. Sign in with your Google account
3. Click your profile picture (top right)
4. Click "Create a channel"
5. Choose "Use a custom name" (not your personal name)
6. Enter your channel name
7. Click "Create"

### Choosing Your Channel Name

Your channel name should be:
- **Memorable**: Easy to remember and spell
- **Relevant**: Related to your niche
- **Unique**: Not too similar to existing channels
- **Searchable**: Contains keywords if possible

**Examples by Niche:**
- Finance: "Money Mindset", "Wealth Simplified", "Finance Explained"
- Tech: "Tech Simplified", "AI Daily", "Digital Tools"
- Motivation: "Rise & Grind", "Success Stories", "Daily Motivation"

## Step 2: Channel Branding

### Profile Picture (Channel Icon)

- **Size**: 800 x 800 pixels (displays as circle)
- **Format**: JPG, PNG, or GIF
- **Tips**: Use a logo, icon, or simple graphic that represents your brand

### Banner Image (Channel Art)

- **Size**: 2560 x 1440 pixels (safe area: 1546 x 423 pixels center)
- **Format**: JPG, PNG
- **Include**: Channel name, upload schedule, tagline

### Creating Branding with Free Tools

```python
#!/usr/bin/env python3
"""
Channel Branding Generator
Create profile picture and banner using Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

class BrandingGenerator:
    def __init__(self, channel_name):
        self.channel_name = channel_name
    
    def create_profile_picture(self, output_path, 
                               bg_color=(102, 126, 234),
                               text_color=(255, 255, 255)):
        """Create a simple logo-style profile picture"""
        size = 800
        img = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Get initials
        words = self.channel_name.split()
        initials = ''.join([w[0].upper() for w in words[:2]])
        
        # Draw initials
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 300)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 50
        
        draw.text((x, y), initials, font=font, fill=text_color)
        
        img.save(output_path, quality=95)
        print(f"Profile picture saved: {output_path}")
        return output_path
    
    def create_banner(self, output_path, tagline="", schedule="",
                     bg_colors=[(102, 126, 234), (118, 75, 162)]):
        """Create a gradient banner with channel info"""
        width, height = 2560, 1440
        img = Image.new('RGB', (width, height))
        
        # Create gradient
        for y in range(height):
            ratio = y / height
            r = int(bg_colors[0][0] * (1 - ratio) + bg_colors[1][0] * ratio)
            g = int(bg_colors[0][1] * (1 - ratio) + bg_colors[1][1] * ratio)
            b = int(bg_colors[0][2] * (1 - ratio) + bg_colors[1][2] * ratio)
            
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Channel name
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        # Draw channel name (centered in safe area)
        bbox = draw.textbbox((0, 0), self.channel_name, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 - 100
        
        draw.text((x, y), self.channel_name, font=font_large, fill=(255, 255, 255))
        
        # Draw tagline
        if tagline:
            bbox = draw.textbbox((0, 0), tagline, font=font_medium)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height // 2 + 80
            draw.text((x, y), tagline, font=font_medium, fill=(200, 200, 200))
        
        # Draw schedule
        if schedule:
            bbox = draw.textbbox((0, 0), schedule, font=font_medium)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height // 2 + 160
            draw.text((x, y), schedule, font=font_medium, fill=(180, 180, 180))
        
        img.save(output_path, quality=95)
        print(f"Banner saved: {output_path}")
        return output_path


if __name__ == "__main__":
    generator = BrandingGenerator("AI Productivity")
    
    generator.create_profile_picture("profile_picture.png")
    generator.create_banner(
        "channel_banner.png",
        tagline="Master AI Tools for Maximum Productivity",
        schedule="New Videos Every Monday & Thursday"
    )
```

## Step 3: Channel Description

Write a compelling channel description that:
- Explains what your channel is about
- Tells viewers what they'll learn
- Includes relevant keywords
- Has a call to action

### Template:

```
Welcome to [Channel Name]! 

[One sentence about what you do]

On this channel, you'll discover:
• [Benefit 1]
• [Benefit 2]  
• [Benefit 3]

New videos every [schedule].

Subscribe and hit the notification bell to never miss an update!

[Optional: Links to social media or website]
```

### Example:

```
Welcome to AI Productivity Tips!

We help you work smarter, not harder, using the latest AI tools.

On this channel, you'll discover:
• How to automate repetitive tasks with AI
• The best free AI tools for productivity
• Step-by-step tutorials to 10x your efficiency

New videos every Monday and Thursday at 9 AM EST.

Subscribe and hit the notification bell to transform your workflow!
```

## Step 4: Channel Settings

### Basic Info Settings

1. Go to YouTube Studio (studio.youtube.com)
2. Click "Customization" → "Basic info"
3. Fill in:
   - Channel name
   - Handle (@yourhandle)
   - Description
   - Channel URL
   - Links (social media, website)
   - Contact email

### Branding Settings

1. Click "Customization" → "Branding"
2. Upload:
   - Profile picture
   - Banner image
   - Video watermark (optional, appears on all videos)

### Layout Settings

1. Click "Customization" → "Layout"
2. Set up:
   - Channel trailer (for non-subscribers)
   - Featured video (for returning subscribers)
   - Featured sections (organize your videos)

## Step 5: Default Upload Settings

Save time by setting defaults for all uploads:

1. Go to YouTube Studio
2. Click "Settings" (gear icon)
3. Click "Upload defaults"
4. Set:
   - Title template
   - Description template
   - Tags
   - Category
   - License
   - Comments settings

### Default Description Template:

```
[Video description here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 TIMESTAMPS:
0:00 - Introduction
[Add timestamps]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 SUBSCRIBE for more: [Channel URL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 CONNECT WITH US:
• Twitter: [URL]
• Instagram: [URL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#[niche] #[topic] #[keyword]
```

## Step 6: Playlists

Organize your content into playlists:

1. Go to YouTube Studio
2. Click "Playlists"
3. Click "New playlist"
4. Name it descriptively (include keywords)
5. Add relevant videos

### Playlist Strategy:

- **By Topic**: Group similar content together
- **By Series**: Create numbered series playlists
- **By Difficulty**: Beginner, Intermediate, Advanced
- **By Format**: Tutorials, Reviews, Tips

## Step 7: Channel Verification

Verify your channel to unlock features:

1. Go to YouTube Studio
2. Click "Settings" → "Channel" → "Feature eligibility"
3. Click "Verify" next to your phone number
4. Enter verification code

### Features Unlocked:
- Custom thumbnails
- Videos longer than 15 minutes
- Live streaming
- External links in cards

## Step 8: Monetization Setup (For Later)

Requirements for YouTube Partner Program:
- 1,000 subscribers
- 4,000 watch hours in past 12 months
- OR 10 million Shorts views in 90 days
- Follow YouTube's policies
- Have AdSense account

### Prepare Now:
1. Create Google AdSense account (adsense.google.com)
2. Link it to your YouTube channel
3. Review YouTube's monetization policies

## Channel Setup Checklist

- [ ] Created Brand Account
- [ ] Set channel name
- [ ] Uploaded profile picture (800x800)
- [ ] Uploaded banner (2560x1440)
- [ ] Written channel description
- [ ] Set channel handle (@name)
- [ ] Added contact email
- [ ] Set upload defaults
- [ ] Created initial playlists
- [ ] Verified phone number
- [ ] Reviewed community guidelines

## Common Mistakes to Avoid

1. **Generic channel name**: Be specific to your niche
2. **No upload schedule**: Set expectations for viewers
3. **Missing description**: Hurts discoverability
4. **Poor branding**: Looks unprofessional
5. **No playlists**: Makes content hard to find
6. **Ignoring settings**: Missing optimization opportunities

## Next Steps

1. Complete the channel setup checklist
2. Create your branding assets
3. Write your channel description
4. Set up your first playlist
5. Move to Module 8 for SEO optimization

---

## Additional Resources

- [YouTube Creator Academy](https://creatoracademy.youtube.com/)
- [YouTube Studio Help](https://support.google.com/youtube/answer/9314415)
- [Canva](https://www.canva.com/) - Free design tool for branding
