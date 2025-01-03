from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Directory where videos will be saved
DOWNLOAD_DIR = 'downloads'

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'URL is required'}), 400
    
    # yt-dlp options for downloading video
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # Save to the downloads directory
        'quiet': True,  # Don't show verbose output
    }
    
    try:
        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        
        # Return the path to the downloaded file
        download_link = f'/{filename}'
        return jsonify({'success': True, 'download_link': download_link})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on localhost:5000
