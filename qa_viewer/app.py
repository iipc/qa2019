#!/sur/bin/env python

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
import json

with open("./computations.log.json", "r") as json_input:
    ssim_computation_log = json.load(json_input)

app = Flask(__name__)
app.config["CKEDITOR_SERVE_LOCAL"] = False
app.config["CKEDITOR_HEIGHT"] = 300
app.secret_key = "promise&qa"

bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/code")
def code():
    return render_template("code.html")


@app.route("/lessonslearned")
def lessonslearned():
    return render_template("lessonslearned.html")


@app.route("/firstresults")
def firstresults():
    return render_template(
        "firstresults.html", ssim_computation_log=ssim_computation_log
    )


@app.route("/show/<path:url>", methods=["GET", "POST"])
def show(url):
    return render_template(
        "show_url.html", url=url, data=ssim_computation_log[url]
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
