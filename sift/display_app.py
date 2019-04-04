from flask import Flask
from flask import render_template
app = Flask(__name__)
import json

@app.route("/<result_file>")
def index(result_file):
    with open(result_file) as file:
        context = {
            "results": json.load(file),
            "result_filename": "test.output.json"
            }
    return render_template('index.html', **context)
