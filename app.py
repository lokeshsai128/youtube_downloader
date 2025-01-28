from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import re

app = Flask(__name__)

def get_video_title(video_link):
    result = subprocess.run(['yt-dlp', '--get-title', video_link], capture_output=True, text=True)
    return result.stdout.strip()

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', title)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # Extract form data
    video_link = request.form['video_link']
    video_quality = request.form['video_quality']
    file_type = request.form['file_type']
    
    # Extract video title and sanitize for filename
    video_title = get_video_title(video_link)
    sanitized_title = sanitize_filename(video_title)
    output_filename = os.path.join("D:\Youtube_Downloader\youtube_downloader\YT_Downloaded_Videos", f"{sanitized_title}.mp4")  #please change according to your desired folder path here

    # Construct the script path
    script_path = os.path.join(os.getcwd(), 'download_script.py')

    # Log information for debugging
    print(f"Received request to download video.")
    print(f"Video link: {video_link}")
    print(f"Video quality: {video_quality}")
    print(f"File type: {file_type}")
    print(f"Script path: {script_path}")

    # Run the Python script with the provided parameters
    try:
        result = subprocess.run(['python', script_path, video_link, video_quality, file_type, output_filename], capture_output=True, text=True)
        
        # Log output and errors from the script execution
        print("Script STDOUT:", result.stdout)
        print("Script STDERR:", result.stderr)

        if result.returncode != 0:
            print(f"Script failed with return code {result.returncode}")
            return f"Error: Script failed with return code {result.returncode}"

    except Exception as e:
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}"

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
