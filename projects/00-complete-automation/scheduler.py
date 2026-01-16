"""
KRWUTARTH'S DAILY VIDEO SCHEDULER
=================================
This script runs automatically every day to create and upload videos.
Just start it once and it will keep running forever!

NO MANUAL INTERVENTION REQUIRED!

Usage:
    python scheduler.py

To run in background on Windows:
    pythonw scheduler.py

To stop: Close the window or press Ctrl+C
"""

import os
import sys
import time
import datetime
import threading
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from config import VIDEOS_PER_DAY, SCHEDULE_HOUR, SCHEDULE_MINUTE


def run_automation():
    """Run the video automation script"""
    try:
        logger.info("Starting video automation...")
        
        # Import and run automation
        from auto_video_creator import YouTubeAutomation
        
        automation = YouTubeAutomation()
        success = automation.run()
        
        if success:
            logger.info("Video automation completed successfully!")
        else:
            logger.error("Video automation failed!")
        
        return success
        
    except Exception as e:
        logger.error(f"Error running automation: {e}")
        return False


def get_next_run_time():
    """Calculate the next scheduled run time"""
    now = datetime.datetime.now()
    
    # Create today's scheduled time
    scheduled_time = now.replace(
        hour=SCHEDULE_HOUR,
        minute=SCHEDULE_MINUTE,
        second=0,
        microsecond=0
    )
    
    # If we've passed today's time, schedule for tomorrow
    if now >= scheduled_time:
        scheduled_time += datetime.timedelta(days=1)
    
    return scheduled_time


def wait_until(target_time):
    """Wait until the target time"""
    while True:
        now = datetime.datetime.now()
        if now >= target_time:
            break
        
        # Calculate remaining time
        remaining = (target_time - now).total_seconds()
        
        # Show countdown every hour
        if remaining > 3600:
            hours = int(remaining / 3600)
            logger.info(f"Next video in {hours} hours...")
            time.sleep(3600)  # Sleep for 1 hour
        elif remaining > 60:
            minutes = int(remaining / 60)
            logger.info(f"Next video in {minutes} minutes...")
            time.sleep(60)  # Sleep for 1 minute
        else:
            time.sleep(remaining)


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 60)
    print("   KRWUTARTH'S DAILY VIDEO SCHEDULER")
    print("   Automatic Video Creation & Upload")
    print("=" * 60)
    print(f"\n   Schedule: {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d} every day")
    print(f"   Videos per day: {VIDEOS_PER_DAY}")
    print("\n   Press Ctrl+C to stop")
    print("=" * 60 + "\n")


def main():
    """Main scheduler loop"""
    print_banner()
    
    logger.info("Scheduler started!")
    logger.info(f"Will create {VIDEOS_PER_DAY} video(s) at {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d} daily")
    
    # Ask if user wants to run immediately
    try:
        response = input("\nRun automation now? (y/n): ").strip().lower()
        if response == 'y':
            logger.info("Running automation now...")
            for i in range(VIDEOS_PER_DAY):
                logger.info(f"Creating video {i+1}/{VIDEOS_PER_DAY}...")
                run_automation()
                if i < VIDEOS_PER_DAY - 1:
                    logger.info("Waiting 5 minutes before next video...")
                    time.sleep(300)
    except:
        pass
    
    # Main scheduler loop
    while True:
        try:
            # Get next run time
            next_run = get_next_run_time()
            logger.info(f"Next scheduled run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Wait until scheduled time
            wait_until(next_run)
            
            # Run automation for each video
            for i in range(VIDEOS_PER_DAY):
                logger.info(f"Creating scheduled video {i+1}/{VIDEOS_PER_DAY}...")
                run_automation()
                
                # Wait between videos
                if i < VIDEOS_PER_DAY - 1:
                    logger.info("Waiting 10 minutes before next video...")
                    time.sleep(600)
            
            logger.info("Daily videos completed!")
            
        except KeyboardInterrupt:
            logger.info("\nScheduler stopped by user.")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            logger.info("Retrying in 1 hour...")
            time.sleep(3600)


if __name__ == "__main__":
    main()
