import subprocess
import sys
import os
import re

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', title)

def download_video(video_url, quality, output_file):
    temp_video_file = 'temp_video.webm'

    # Define command to download video and audio separately
    video_command = [
        'yt-dlp',
        '--format', f'bestvideo[height<={quality}]+bestaudio/best',
        video_url,
        '-o', temp_video_file
    ]

    # Run video download command
    try:
        print(f"Running video command: {' '.join(video_command)}")
        result = subprocess.run(video_command, capture_output=True, text=True)
        print("yt-dlp STDOUT:", result.stdout)
        print("yt-dlp STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"Error downloading video: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"Exception occurred during video download: {e}")
        sys.exit(1)

    # Debugging: Check if video file exists
    if not os.path.exists(temp_video_file):
        print(f"Video file not found: {temp_video_file}")
        sys.exit(1)

    # Define merge command
    merge_command = [
        'ffmpeg',
        '-i', temp_video_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]

    # Run merge command
    try:
        print(f"Running merge command: {' '.join(merge_command)}")
        result = subprocess.run(merge_command, capture_output=True, text=True)
        print("ffmpeg STDOUT:", result.stdout)
        print("ffmpeg STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"Error merging files: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"Exception occurred during merging: {e}")
        sys.exit(1)

    # Clean up temporary files
    if os.path.exists(temp_video_file):
        os.remove(temp_video_file)

def download_audio(video_url, output_file):
    audio_file = 'temp_audio.m4a'

    # Define command to download audio
    audio_command = [
        'yt-dlp',
        '--format', 'bestaudio',
        video_url,
        '-o', audio_file
    ]

    # Run audio download command
    try:
        print(f"Running audio command: {' '.join(audio_command)}")
        result = subprocess.run(audio_command, capture_output=True, text=True)
        print("yt-dlp STDOUT:", result.stdout)
        print("yt-dlp STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"Error downloading audio: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"Exception occurred during audio download: {e}")
        sys.exit(1)

    # Convert audio to mp3 format
    convert_command = [
        'ffmpeg',
        '-i', audio_file,
        '-codec:a', 'libmp3lame',
        output_file
    ]

    try:
        print(f"Running convert command: {' '.join(convert_command)}")
        result = subprocess.run(convert_command, capture_output=True, text=True)
        print("ffmpeg STDOUT:", result.stdout)
        print("ffmpeg STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"Error converting audio: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"Exception occurred during audio conversion: {e}")
        sys.exit(1)

    # Clean up temporary files
    if os.path.exists(audio_file):
        os.remove(audio_file)

def main():
    if len(sys.argv) != 5:
        print("Usage: python download_script.py <video_url> <quality> <file_type> <output_file>")
        sys.exit(1)

    video_url = sys.argv[1]
    quality = sys.argv[2].strip('<>')  # Remove angle brackets if present
    file_type = sys.argv[3]
    output_file = sys.argv[4]

    print(f"Starting download for URL: {video_url}, Quality: {quality}, Type: {file_type}, Output: {output_file}")

    if file_type == 'video':
        download_video(video_url, quality, output_file)
    elif file_type == 'audio':
        download_audio(video_url, output_file)
    else:
        print("Invalid file type. Choose 'video' or 'audio'.")
        sys.exit(1)

if __name__ == '__main__':
    main()
