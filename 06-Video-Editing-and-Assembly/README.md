# Module 6: Video Editing and Assembly (Free Tools)

## Overview

This module teaches you how to edit and assemble your faceless YouTube videos using completely free tools. We'll cover both manual editing with DaVinci Resolve and automated editing with Python scripts.

## Free Video Editing Options

### Option 1: DaVinci Resolve (Manual Editing)
- **Cost**: 100% Free
- **Best For**: High-quality manual editing
- **Download**: https://www.blackmagicdesign.com/products/davinciresolve

### Option 2: MoviePy (Automated with Python)
- **Cost**: 100% Free
- **Best For**: Batch processing, automation
- **Install**: `pip install moviepy`

### Option 3: Kdenlive (Manual Editing)
- **Cost**: 100% Free, Open Source
- **Best For**: Linux users, simpler interface
- **Download**: https://kdenlive.org/

### Option 4: OpenShot (Manual Editing)
- **Cost**: 100% Free
- **Best For**: Beginners
- **Download**: https://www.openshot.org/

## Automated Video Assembly with MoviePy

### Installation

```bash
pip install moviepy
pip install Pillow
```

### Basic Video Assembly Script

```python
#!/usr/bin/env python3
"""
Basic Video Assembler
Combines voiceover with background footage
"""

from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, TextClip, ColorClip
)
import os

class VideoAssembler:
    def __init__(self, output_width=1920, output_height=1080):
        self.width = output_width
        self.height = output_height
    
    def create_simple_video(self, audio_file, video_file, output_file):
        """
        Create a simple video with audio over video footage
        
        Parameters:
        - audio_file: Path to voiceover MP3
        - video_file: Path to background video
        - output_file: Path for output video
        """
        print(f"Loading audio: {audio_file}")
        audio = AudioFileClip(audio_file)
        audio_duration = audio.duration
        
        print(f"Loading video: {video_file}")
        video = VideoFileClip(video_file)
        
        # Loop video if shorter than audio
        if video.duration < audio_duration:
            loops_needed = int(audio_duration / video.duration) + 1
            video = concatenate_videoclips([video] * loops_needed)
        
        # Trim video to match audio length
        video = video.subclip(0, audio_duration)
        
        # Resize video to target dimensions
        video = video.resize((self.width, self.height))
        
        # Add audio to video
        final_video = video.set_audio(audio)
        
        print(f"Rendering video: {output_file}")
        final_video.write_videofile(
            output_file,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Clean up
        audio.close()
        video.close()
        
        print(f"Done! Video saved to: {output_file}")
        return output_file


if __name__ == "__main__":
    assembler = VideoAssembler()
    
    # Example usage
    assembler.create_simple_video(
        audio_file="voiceover.mp3",
        video_file="background.mp4",
        output_file="final_video.mp4"
    )
```

### Advanced Video Assembly with Multiple Clips

```python
#!/usr/bin/env python3
"""
Advanced Video Assembler
Combines multiple video clips with voiceover sections
"""

from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, TextClip, ColorClip,
    CompositeAudioClip, concatenate_audioclips
)
import os
import json

class AdvancedVideoAssembler:
    def __init__(self, width=1920, height=1080, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
    
    def load_and_resize_video(self, video_path, duration=None):
        """Load a video and resize to target dimensions"""
        video = VideoFileClip(video_path)
        video = video.resize((self.width, self.height))
        
        if duration and video.duration > duration:
            video = video.subclip(0, duration)
        
        return video
    
    def create_text_overlay(self, text, duration, fontsize=70, 
                           color='white', bg_color='black'):
        """Create a text overlay clip"""
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color=color,
            font='DejaVu-Sans-Bold',
            size=(self.width - 100, None),
            method='caption'
        )
        txt_clip = txt_clip.set_duration(duration)
        txt_clip = txt_clip.set_position('center')
        
        return txt_clip
    
    def assemble_from_sections(self, sections, output_file):
        """
        Assemble video from multiple sections
        
        sections: List of dicts with:
            - audio: path to audio file
            - video: path to video file (or list of videos)
            - text: optional text overlay
        """
        clips = []
        
        for i, section in enumerate(sections):
            print(f"Processing section {i+1}/{len(sections)}")
            
            # Load audio
            audio = AudioFileClip(section['audio'])
            duration = audio.duration
            
            # Load video(s)
            if isinstance(section['video'], list):
                # Multiple videos - concatenate them
                video_clips = []
                remaining_duration = duration
                
                for video_path in section['video']:
                    if remaining_duration <= 0:
                        break
                    
                    clip = self.load_and_resize_video(video_path)
                    clip_duration = min(clip.duration, remaining_duration)
                    clip = clip.subclip(0, clip_duration)
                    video_clips.append(clip)
                    remaining_duration -= clip_duration
                
                video = concatenate_videoclips(video_clips)
            else:
                # Single video - loop if needed
                video = self.load_and_resize_video(section['video'])
                
                if video.duration < duration:
                    loops = int(duration / video.duration) + 1
                    video = concatenate_videoclips([video] * loops)
                
                video = video.subclip(0, duration)
            
            # Add text overlay if specified
            if section.get('text'):
                txt_clip = self.create_text_overlay(
                    section['text'],
                    duration=min(5, duration),  # Show text for 5 seconds max
                    fontsize=section.get('fontsize', 70)
                )
                video = CompositeVideoClip([video, txt_clip])
            
            # Set audio
            video = video.set_audio(audio)
            clips.append(video)
        
        # Concatenate all sections
        print("Concatenating all sections...")
        final_video = concatenate_videoclips(clips, method='compose')
        
        # Render
        print(f"Rendering final video: {output_file}")
        final_video.write_videofile(
            output_file,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            threads=4
        )
        
        # Clean up
        for clip in clips:
            clip.close()
        
        print(f"Done! Video saved to: {output_file}")
        return output_file
    
    def add_intro_outro(self, main_video, intro_video=None, outro_video=None, output_file=None):
        """Add intro and outro to a video"""
        clips = []
        
        if intro_video:
            intro = VideoFileClip(intro_video).resize((self.width, self.height))
            clips.append(intro)
        
        main = VideoFileClip(main_video).resize((self.width, self.height))
        clips.append(main)
        
        if outro_video:
            outro = VideoFileClip(outro_video).resize((self.width, self.height))
            clips.append(outro)
        
        final = concatenate_videoclips(clips)
        
        output = output_file or main_video.replace('.mp4', '_with_intro_outro.mp4')
        final.write_videofile(output, fps=self.fps, codec='libx264', audio_codec='aac')
        
        return output


# Example usage
if __name__ == "__main__":
    assembler = AdvancedVideoAssembler()
    
    # Define video sections
    sections = [
        {
            "audio": "voiceovers/intro.mp3",
            "video": "footage/intro_background.mp4",
            "text": "5 AI Tools That Will Change Your Life"
        },
        {
            "audio": "voiceovers/section1.mp3",
            "video": ["footage/tech1.mp4", "footage/tech2.mp4"],
        },
        {
            "audio": "voiceovers/section2.mp3",
            "video": "footage/office.mp4",
        },
        {
            "audio": "voiceovers/outro.mp3",
            "video": "footage/outro_background.mp4",
            "text": "Subscribe for more!"
        }
    ]
    
    assembler.assemble_from_sections(sections, "final_video.mp4")
```

### Adding Background Music

```python
#!/usr/bin/env python3
"""
Add Background Music to Video
Mixes voiceover with background music at appropriate levels
"""

from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeAudioClip,
    afx
)

def add_background_music(video_file, music_file, output_file, 
                         music_volume=0.1):
    """
    Add background music to a video
    
    Parameters:
    - video_file: Path to video with voiceover
    - music_file: Path to background music
    - output_file: Path for output
    - music_volume: Volume of music (0.0 to 1.0, default 0.1 = 10%)
    """
    print("Loading video...")
    video = VideoFileClip(video_file)
    original_audio = video.audio
    
    print("Loading music...")
    music = AudioFileClip(music_file)
    
    # Loop music if shorter than video
    if music.duration < video.duration:
        loops = int(video.duration / music.duration) + 1
        from moviepy.editor import concatenate_audioclips
        music = concatenate_audioclips([music] * loops)
    
    # Trim music to video length
    music = music.subclip(0, video.duration)
    
    # Reduce music volume
    music = music.volumex(music_volume)
    
    # Fade in/out music
    music = afx.audio_fadein(music, 2)  # 2 second fade in
    music = afx.audio_fadeout(music, 3)  # 3 second fade out
    
    # Combine voiceover and music
    print("Mixing audio...")
    combined_audio = CompositeAudioClip([original_audio, music])
    
    # Set combined audio to video
    final_video = video.set_audio(combined_audio)
    
    print(f"Rendering: {output_file}")
    final_video.write_videofile(
        output_file,
        fps=30,
        codec='libx264',
        audio_codec='aac'
    )
    
    video.close()
    music.close()
    
    print("Done!")
    return output_file


if __name__ == "__main__":
    add_background_music(
        video_file="video_with_voiceover.mp4",
        music_file="background_music.mp3",
        output_file="final_with_music.mp4",
        music_volume=0.15  # 15% volume for music
    )
```

### Creating Title Cards and Transitions

```python
#!/usr/bin/env python3
"""
Create Title Cards and Transitions
Generate professional-looking title screens
"""

from moviepy.editor import (
    ColorClip, TextClip, CompositeVideoClip,
    concatenate_videoclips
)
from moviepy.video.fx.all import fadein, fadeout

class TitleCardGenerator:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
    
    def create_title_card(self, title, subtitle=None, duration=5,
                         bg_color=(20, 20, 40), text_color='white'):
        """Create a title card with optional subtitle"""
        
        # Background
        bg = ColorClip(
            size=(self.width, self.height),
            color=bg_color,
            duration=duration
        )
        
        # Title text
        title_clip = TextClip(
            title,
            fontsize=90,
            color=text_color,
            font='DejaVu-Sans-Bold'
        )
        title_clip = title_clip.set_position(('center', self.height//2 - 80))
        title_clip = title_clip.set_duration(duration)
        
        clips = [bg, title_clip]
        
        # Subtitle if provided
        if subtitle:
            sub_clip = TextClip(
                subtitle,
                fontsize=50,
                color='gray',
                font='DejaVu-Sans'
            )
            sub_clip = sub_clip.set_position(('center', self.height//2 + 40))
            sub_clip = sub_clip.set_duration(duration)
            clips.append(sub_clip)
        
        # Composite
        final = CompositeVideoClip(clips)
        
        # Add fade effects
        final = fadein(final, 1)
        final = fadeout(final, 1)
        
        return final
    
    def create_section_title(self, number, title, duration=3,
                            bg_color=(30, 60, 90)):
        """Create a section title card (e.g., "1. First Topic")"""
        
        bg = ColorClip(
            size=(self.width, self.height),
            color=bg_color,
            duration=duration
        )
        
        # Number
        num_clip = TextClip(
            str(number),
            fontsize=200,
            color='white',
            font='DejaVu-Sans-Bold'
        )
        num_clip = num_clip.set_position((self.width//4, 'center'))
        num_clip = num_clip.set_duration(duration)
        
        # Title
        title_clip = TextClip(
            title,
            fontsize=70,
            color='white',
            font='DejaVu-Sans'
        )
        title_clip = title_clip.set_position((self.width//2, 'center'))
        title_clip = title_clip.set_duration(duration)
        
        final = CompositeVideoClip([bg, num_clip, title_clip])
        final = fadein(final, 0.5)
        final = fadeout(final, 0.5)
        
        return final
    
    def create_end_screen(self, channel_name, duration=10,
                         bg_color=(20, 20, 40)):
        """Create an end screen with subscribe prompt"""
        
        bg = ColorClip(
            size=(self.width, self.height),
            color=bg_color,
            duration=duration
        )
        
        # Thanks message
        thanks = TextClip(
            "Thanks for Watching!",
            fontsize=80,
            color='white',
            font='DejaVu-Sans-Bold'
        )
        thanks = thanks.set_position(('center', self.height//3))
        thanks = thanks.set_duration(duration)
        
        # Subscribe prompt
        subscribe = TextClip(
            "SUBSCRIBE for more content",
            fontsize=50,
            color='red',
            font='DejaVu-Sans-Bold'
        )
        subscribe = subscribe.set_position(('center', self.height//2))
        subscribe = subscribe.set_duration(duration)
        
        # Channel name
        channel = TextClip(
            channel_name,
            fontsize=40,
            color='gray',
            font='DejaVu-Sans'
        )
        channel = channel.set_position(('center', self.height*2//3))
        channel = channel.set_duration(duration)
        
        final = CompositeVideoClip([bg, thanks, subscribe, channel])
        final = fadein(final, 1)
        final = fadeout(final, 2)
        
        return final


if __name__ == "__main__":
    generator = TitleCardGenerator()
    
    # Create intro title
    intro = generator.create_title_card(
        title="10 AI Tools for Productivity",
        subtitle="That Will Save You Hours Every Day",
        duration=5
    )
    intro.write_videofile("intro_title.mp4", fps=30)
    
    # Create section titles
    sections = [
        (1, "ChatGPT for Writing"),
        (2, "Notion AI for Notes"),
        (3, "Grammarly for Editing"),
    ]
    
    for num, title in sections:
        card = generator.create_section_title(num, title)
        card.write_videofile(f"section_{num}_title.mp4", fps=30)
    
    # Create end screen
    end = generator.create_end_screen("AI Productivity Channel")
    end.write_videofile("end_screen.mp4", fps=30)
```

## Complete Video Production Pipeline

```python
#!/usr/bin/env python3
"""
Complete Video Production Pipeline
Assembles all components into a final video
"""

from moviepy.editor import *
import os
import json

class VideoProductionPipeline:
    def __init__(self, project_dir, width=1920, height=1080):
        self.project_dir = project_dir
        self.width = width
        self.height = height
        
        # Create output directories
        self.dirs = {
            'scripts': os.path.join(project_dir, 'scripts'),
            'voiceovers': os.path.join(project_dir, 'voiceovers'),
            'footage': os.path.join(project_dir, 'footage'),
            'titles': os.path.join(project_dir, 'titles'),
            'output': os.path.join(project_dir, 'output')
        }
        
        for d in self.dirs.values():
            os.makedirs(d, exist_ok=True)
    
    def produce_video(self, config):
        """
        Produce a complete video from configuration
        
        config: dict with:
            - title: Video title
            - sections: List of section configs
            - background_music: Optional music file
            - channel_name: For end screen
        """
        clips = []
        
        # 1. Create intro title card
        print("Creating intro...")
        intro = self._create_title_card(
            config['title'],
            config.get('subtitle', ''),
            duration=5
        )
        clips.append(intro)
        
        # 2. Process each section
        for i, section in enumerate(config['sections']):
            print(f"Processing section {i+1}...")
            
            # Section title card
            if section.get('title'):
                section_title = self._create_section_title(
                    i + 1,
                    section['title']
                )
                clips.append(section_title)
            
            # Main content
            audio_path = section['audio']
            video_paths = section['video']
            
            content = self._create_section_content(audio_path, video_paths)
            clips.append(content)
        
        # 3. Create end screen
        print("Creating end screen...")
        end_screen = self._create_end_screen(
            config.get('channel_name', 'My Channel')
        )
        clips.append(end_screen)
        
        # 4. Concatenate all clips
        print("Assembling video...")
        final_video = concatenate_videoclips(clips, method='compose')
        
        # 5. Add background music if provided
        if config.get('background_music'):
            print("Adding background music...")
            final_video = self._add_background_music(
                final_video,
                config['background_music']
            )
        
        # 6. Render final video
        output_path = os.path.join(
            self.dirs['output'],
            f"{config['title'].replace(' ', '_')}.mp4"
        )
        
        print(f"Rendering final video: {output_path}")
        final_video.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            threads=4
        )
        
        # Clean up
        final_video.close()
        for clip in clips:
            clip.close()
        
        print(f"Done! Video saved to: {output_path}")
        return output_path
    
    def _create_title_card(self, title, subtitle, duration=5):
        """Create intro title card"""
        bg = ColorClip(
            size=(self.width, self.height),
            color=(20, 20, 40),
            duration=duration
        )
        
        title_txt = TextClip(
            title,
            fontsize=80,
            color='white',
            font='DejaVu-Sans-Bold'
        ).set_position(('center', self.height//2 - 60)).set_duration(duration)
        
        clips = [bg, title_txt]
        
        if subtitle:
            sub_txt = TextClip(
                subtitle,
                fontsize=45,
                color='gray',
                font='DejaVu-Sans'
            ).set_position(('center', self.height//2 + 40)).set_duration(duration)
            clips.append(sub_txt)
        
        return CompositeVideoClip(clips).fadein(1).fadeout(1)
    
    def _create_section_title(self, number, title, duration=3):
        """Create section title card"""
        bg = ColorClip(
            size=(self.width, self.height),
            color=(30, 60, 90),
            duration=duration
        )
        
        txt = TextClip(
            f"{number}. {title}",
            fontsize=70,
            color='white',
            font='DejaVu-Sans-Bold'
        ).set_position('center').set_duration(duration)
        
        return CompositeVideoClip([bg, txt]).fadein(0.5).fadeout(0.5)
    
    def _create_section_content(self, audio_path, video_paths):
        """Create section content with audio and video"""
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        if isinstance(video_paths, str):
            video_paths = [video_paths]
        
        # Load and concatenate videos
        video_clips = []
        remaining = duration
        
        for vpath in video_paths:
            if remaining <= 0:
                break
            
            clip = VideoFileClip(vpath).resize((self.width, self.height))
            clip_dur = min(clip.duration, remaining)
            video_clips.append(clip.subclip(0, clip_dur))
            remaining -= clip_dur
        
        # Loop last clip if needed
        if remaining > 0 and video_clips:
            last_clip = video_clips[-1]
            loops = int(remaining / last_clip.duration) + 1
            extended = concatenate_videoclips([last_clip] * loops)
            video_clips[-1] = extended.subclip(0, video_clips[-1].duration + remaining)
        
        video = concatenate_videoclips(video_clips)
        video = video.subclip(0, duration)
        
        return video.set_audio(audio)
    
    def _create_end_screen(self, channel_name, duration=8):
        """Create end screen"""
        bg = ColorClip(
            size=(self.width, self.height),
            color=(20, 20, 40),
            duration=duration
        )
        
        thanks = TextClip(
            "Thanks for Watching!",
            fontsize=70,
            color='white',
            font='DejaVu-Sans-Bold'
        ).set_position(('center', self.height//3)).set_duration(duration)
        
        subscribe = TextClip(
            "SUBSCRIBE",
            fontsize=60,
            color='red',
            font='DejaVu-Sans-Bold'
        ).set_position(('center', self.height//2)).set_duration(duration)
        
        return CompositeVideoClip([bg, thanks, subscribe]).fadein(1).fadeout(2)
    
    def _add_background_music(self, video, music_path, volume=0.1):
        """Add background music to video"""
        music = AudioFileClip(music_path)
        
        if music.duration < video.duration:
            loops = int(video.duration / music.duration) + 1
            music = concatenate_audioclips([music] * loops)
        
        music = music.subclip(0, video.duration).volumex(volume)
        music = audio_fadein(music, 2)
        music = audio_fadeout(music, 3)
        
        combined = CompositeAudioClip([video.audio, music])
        return video.set_audio(combined)


# Example usage
if __name__ == "__main__":
    pipeline = VideoProductionPipeline("my_video_project")
    
    config = {
        "title": "5 AI Tools That Will Change Your Life",
        "subtitle": "Boost Your Productivity Today",
        "channel_name": "AI Productivity Tips",
        "background_music": "music/background.mp3",  # Optional
        "sections": [
            {
                "title": "ChatGPT",
                "audio": "voiceovers/section1.mp3",
                "video": ["footage/chatgpt1.mp4", "footage/chatgpt2.mp4"]
            },
            {
                "title": "Notion AI",
                "audio": "voiceovers/section2.mp3",
                "video": "footage/notion.mp4"
            },
            {
                "title": "Grammarly",
                "audio": "voiceovers/section3.mp3",
                "video": "footage/grammarly.mp4"
            }
        ]
    }
    
    pipeline.produce_video(config)
```

## Free Background Music Sources

- **YouTube Audio Library**: https://studio.youtube.com/channel/UC/music (free for YouTube videos)
- **Pixabay Music**: https://pixabay.com/music/ (free, no attribution)
- **Mixkit Music**: https://mixkit.co/free-stock-music/ (free)
- **Bensound**: https://www.bensound.com/ (free with attribution)

## Quality Checklist

Before exporting your final video:

- [ ] Audio levels are balanced (voiceover louder than music)
- [ ] No audio clipping or distortion
- [ ] Video resolution is 1080p or higher
- [ ] Transitions are smooth
- [ ] Text is readable
- [ ] No copyright issues with footage or music
- [ ] Video length is appropriate (8-15 minutes ideal)
- [ ] End screen has subscribe prompt

## Next Steps

1. Practice with the basic video assembler
2. Create your first complete video using the pipeline
3. Experiment with different title card styles
4. Move to Module 7 for YouTube channel setup

---

## Additional Resources

- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [DaVinci Resolve Tutorials](https://www.blackmagicdesign.com/products/davinciresolve/training)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
