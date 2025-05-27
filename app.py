from flask import Flask, request, render_template_string
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Downloader</title>
</head>
<body style="text-align:center; margin-top:50px;">
    <h1>YouTube Downloader</h1>
    <form method="post">
        <input type="text" name="url" placeholder="Enter YouTube URL" size="50" required>
        <button type="submit">Fetch Formats</button>
    </form>
    {% if formats %}
        <h2>Available Formats</h2>
        <ul>
        {% for f in formats %}
            <li>
                <a href="{{ f.url }}" target="_blank">
                    {{ f.ext }} | {{ f.format_note }} | {{ f.resolution }}
                </a>
            </li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    formats = []
    if request.method == "POST":
        url = request.form["url"]
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            for f in info.get("formats", []):
                if f.get("url") and f.get("ext"):
                    formats.append({
                        "url": f["url"],
                        "ext": f["ext"],
                        "format_note": f.get("format_note", ""),
                        "resolution": f.get("resolution", "")
                    })
    return render_template_string(HTML_TEMPLATE, formats=formats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
