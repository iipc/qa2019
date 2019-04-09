import requests
from bs4 import BeautifulSoup
from uuid import uuid4

def fetch(url, output_path="/tmp/", screenshot_method=1, timeout_duration=100):
    html_doc = requests.get(url).text
    output = BeautifulSoup(html_doc, 'html.parser')
    output_path = "{}{}.txt".format(output_path, uuid4())
    with open(output_path, 'w') as tmpfile:
        tmpfile.write(output.get_text())
    return open(output_path)
