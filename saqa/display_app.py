from flask import Flask
from flask import render_template, send_from_directory
import json


app = Flask(__name__)
app.config["SCREENSHOTS_DIRECTORY"] = '/home/manu/projets/promise/explorations/screenshots_qc'

@app.route("/<result_file>")
def index(result_file):
    with open(result_file) as file:
        context = {
            "results": json.load(file),
            "result_filename": "test.output.json"
            }
    return render_template('index.html', **context)

@app.route('/screenshot/<path:filename>')
def screenshot_static(filename):
    return send_from_directory(app.config['SCREENSHOTS_DIRECTORY'], filename)
