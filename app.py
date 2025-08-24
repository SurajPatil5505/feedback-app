from flask import Flask, render_template, request, redirect, send_from_directory, Response, stream_with_context
import os, base64, webbrowser, threading, time
from datetime import datetime
from werkzeug.exceptions import RequestEntityTooLarge
from dotenv import load_dotenv
from generate_feedback_card import generate_card
# from linkedin import post_to_linkedin  # Uncomment if used

load_dotenv()

app = Flask(__name__)
# Allow up to 10 MB payloads
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

LOGO_PATH = "images/ifm.jfif"
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(e):
    return "Image too large. Please recapture at lower resolution.", 413

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        feedback = request.form.get("feedback")
        image_data = request.form.get("image_data")

        if not image_data or not image_data.startswith("data:image"):
            return "Invalid image data", 400

        # Decode Base64 payload
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        raw_filename = f"{name}_{timestamp}.jpg"
        raw_path = os.path.join(UPLOAD_FOLDER, "raw_" + raw_filename)
        final_path = os.path.join(UPLOAD_FOLDER, "final_" + raw_filename)

        # Save raw upload
        with open(raw_path, "wb") as f:
            f.write(image_bytes)

        # Generate styled feedback card
        generate_card(raw_path, LOGO_PATH, name, feedback, final_path)

        # Log feedback
        with open("feedback_log.txt", "a") as log:
            log.write(f"{timestamp} | {name}: {feedback} | {final_path}\n")

        # Post to LinkedIn
        # post_to_linkedin(final_path)

        return redirect("/")

    return render_template("index.html")

@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/viewer")
def viewer():
    files = sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith("final_")],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
        reverse=True
    )
    file_urls = [f"/static/uploads/{f}" for f in files]
    return render_template("viewer.html", file_urls=file_urls)

@app.route("/events")
def events():
    def event_stream():
        files = sorted(
            [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith("final_")],
            key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
            reverse=True
        )
        last_sent = files[0] if files else None

        while True:
            files = sorted(
                [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith("final_")],
                key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)),
                reverse=True
            )
            if files:
                latest = files[0]
                if latest != last_sent:
                    last_sent = latest
                    yield f"data: /static/uploads/{latest}\n\n"
            time.sleep(2)
    return Response(stream_with_context(event_stream()), content_type="text/event-stream")

if __name__ == "__main__":
    # Use 0.0.0.0 to listen on all interfaces
    def open_browser():
        webbrowser.open_new("http://localhost:5000")

    threading.Timer(1.25, open_browser).start()
    app.run(host="0.0.0.0", port=5000)