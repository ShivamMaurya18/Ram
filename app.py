# app.py
from dotenv import load_dotenv
load_dotenv()  # .env file load karo — sabse pehle

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.numerology import get_numerology_data
from utils.image_utils import generate_poster
from utils.ai_utils    import generate_blessing_message

app = Flask(__name__)
app.secret_key = "ram-navami-2026-secret"

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXT   = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"]        = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"]   = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name", "").strip()
    dob  = request.form.get("dob",  "").strip()

    if not name or not dob:
        flash("Please enter your name and date of birth.", "error")
        return redirect(url_for("index"))

    if "photo" not in request.files or request.files["photo"].filename == "":
        flash("Please upload your photo.", "error")
        return redirect(url_for("index"))

    photo = request.files["photo"]
    if not allowed_file(photo.filename):
        flash("Only PNG / JPG / JPEG / WEBP images are allowed.", "error")
        return redirect(url_for("index"))

    filename  = secure_filename(photo.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    photo.save(save_path)

    # Numerology
    mulank_data = get_numerology_data(dob)

    # Blessing — fully offline
    blessing = generate_blessing_message(name, mulank_data)

    # Generate poster (OpenAI Ghibli style inside)
    try:
        poster_rel_path = generate_poster(save_path, name, blessing, mulank_data)
    except Exception as e:
        flash(f"Poster generation failed: {e}", "error")
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        name        = name,
        poster_path = poster_rel_path,
        blessing    = blessing,
        mulank_data = mulank_data,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)