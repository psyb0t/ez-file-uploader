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
)

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
SECRET_KEY = "your_secret_key_here"
CORRECT_PASSWORD = config.UPLOAD_PASSWORD

PWD_PARAM_NAME = "pwd"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def upload_file():
    authenticated = False

    password = request.args.get(PWD_PARAM_NAME)
    if password and password == CORRECT_PASSWORD:
        authenticated = True

    if request.method == "POST" and "file" in request.files and authenticated:
        file = request.files["file"]
        if file:
            filename = f"{int(round(time.time() * 1000))}-{file.filename}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            flash("File successfully uploaded!")

            print(f'{url_for("upload_file")}?{PWD_PARAM_NAME}={password}')

            return redirect(f'{url_for("upload_file")}?{PWD_PARAM_NAME}={password}')

    return render_template("index.html", authenticated=authenticated, pwd=password)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
