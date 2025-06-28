from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "Please provide a YouTube URL."

        unique_id = uuid.uuid4().hex
        output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            mp3_file = output_template.replace("%(ext)s", "mp3")
            return send_file(mp3_file, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}"

    return render_template("index.html")

app.run(host="0.0.0.0", port=81)
