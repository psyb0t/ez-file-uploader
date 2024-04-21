import os
import time
import config

from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    session,
)

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
SECRET_KEY = "your_secret_key_here"
CORRECT_PASSWORD = config.UPLOAD_PASSWORD

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = SECRET_KEY  # Needed for flashing messages and secure cookies


@app.route("/", methods=["GET", "POST"])
def upload_file():
    # Check if user is already authenticated via cookie
    if not session.get("authenticated"):
        # Authenticate the user
        if request.method == "POST" and "password" in request.form:
            password = request.form["password"]
            if password == CORRECT_PASSWORD:
                session["authenticated"] = True  # Set session as authenticated
                flash("Authenticated successfully!")
            else:
                flash("Authentication failed!")

                return redirect(url_for("upload_file"))

    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        if file:
            filename = f"{int(round(time.time() * 1000))}-{file.filename}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            flash("File successfully uploaded!")

            return redirect(url_for("upload_file"))

    return render_template("index.html", authenticated=session.get("authenticated"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
