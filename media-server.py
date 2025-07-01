from flask import Flask, jsonify, send_file
import subprocess
import requests
import os
from urllib.parse import urlparse, unquote
from PIL import Image
import io

app = Flask(__name__)

def get_media_info():
    try:
        title = subprocess.check_output(['playerctl', 'metadata', 'xesam:title']).decode('utf-8').strip()
        artist = subprocess.check_output(['playerctl', 'metadata', 'xesam:artist']).decode('utf-8').strip()
        album = subprocess.check_output(['playerctl', 'metadata', 'xesam:album']).decode('utf-8').strip()
        art_url = subprocess.check_output(['playerctl', 'metadata', 'mpris:artUrl']).decode('utf-8').strip()
        status = subprocess.check_output(['playerctl','status']).decode('utf-8').strip()
        #print(art_url)
        art_path = None
        art_source = None

        if art_url.startswith("http://") or art_url.startswith("https://"):
            response = requests.get(art_url)
            if response.status_code == 200:
                with open("/tmp/album_art.jpg", "wb") as f:
                    f.write(response.content)
                art_path = "/tmp/album_art.jpg"
                art_source = "url"
        elif art_url.startswith("file:///"):
            parsed = urlparse(art_url)
            art_path = unquote(parsed.path)
            art_source = "file"

        return {
            "title": title,
            "artist": artist,
            "album": album,
            "art_path": art_path,
            "status": status,
            "art_source": art_source
        }

    except subprocess.CalledProcessError:
        return None

@app.route('/now_playing')
def now_playing():
    media_info = get_media_info()
    if media_info:
        return jsonify({
            "title": media_info["title"],
            "artist": media_info["artist"],
            "album": media_info["album"],
            "is_playing": True,
            "status": media_info["status"],
            "art_source": media_info["art_source"]
        })
    else:
        return jsonify({"error": "No media playing"}), 404

@app.route('/album_art')
def album_art():
    info = get_media_info()
    art_path = info.get("art_path") if info else None

    if art_path and os.path.exists(art_path):
        try:
            if art_path.lower().endswith((".jpg", ".jpeg")):
                return send_file(art_path, mimetype='image/jpeg')
            else:
                with Image.open(art_path) as img:
                    img = img.convert("RGB")
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG")
                    buffer.seek(0)
                    return send_file(buffer, mimetype='image/jpeg')
        except Exception as e:
            return f"Image processing error: {e}", 500

    return "No album art", 404

@app.route('/toggle_play', methods=['POST'])
def toggle_play():
    os.system("playerctl play-pause")
    return jsonify({"status": "toggled"})

@app.route('/skip', methods=['POST'])
def skip():
    os.system("playerctl next")
    return jsonify({"Status": "skipped"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
