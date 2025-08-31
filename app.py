import os
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask setup
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXT = {"png","jpg","jpeg","webp"}
MAX_MB = 10

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_MB * 1024 * 1024
app.secret_key = os.environ.get("SECRET_KEY","dev")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXT

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    if "photo" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["photo"]
    user_desc = request.form.get("desc","").strip()

    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))
    if not allowed_file(file.filename):
        flash("Unsupported file type")
        return redirect(url_for("index"))

    fname = secure_filename(file.filename)
    fpath = os.path.join(app.config["UPLOAD_FOLDER"], fname)
    file.save(fpath)

    try:
        # Open and resize image to a smaller size before sending to API
        img = Image.open(fpath)
        max_size = (512, 512)
        img.thumbnail(max_size)

        prompt = f"""
        You are an Instagram caption generator.
        Context: {user_desc}.
        Task:
        1. Analyze the image and description.
        2. Create 4 different catchy captions (each under 140 chars) with different vibes:
           - One fun/casual
           - One inspiring/motivational  
           - One trendy/cool
           - One heartfelt/emotional
        3. Generate 8–12 natural hashtags related to scene + mood + vibe.
        Output ONLY valid JSON (no markdown, no code fences):
        {{
          "captions": [
            "caption 1...",
            "caption 2...", 
            "caption 3...",
            "caption 4..."
          ],
          "hashtags": ["#...", "#..."]
        }}
        """

        response = model.generate_content([prompt, img])
        content = response.text
        print("Gemini raw output:", content)

        import json
        try:
            cleaned = content.strip().strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            result = json.loads(cleaned)
            captions = result.get("captions", [])  # Now expecting multiple captions
            hashtags = result.get("hashtags", [])
        except Exception:
            captions = [content]  # Fallback to single caption
            hashtags = []

    except Exception as e:
        flash(f"AI error: {e}")
        return redirect(url_for("index"))

    return render_template("result.html", image_filename=fname, captions=captions, hashtags=hashtags)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)