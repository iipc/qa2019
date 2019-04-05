import requests
import shutil
import urllib
from uuid import uuid4
import logging

def fetch(url, source="original", output_path="/tmp/", screenshot_method=1, timeout_duration=100):
    api_url = "https://beta.webarchive.org.uk/access/screenshot/?type=screenshot&source={}&url={}".format(source, urllib.parse.quote_plus(url))
    logging.info("webarchive API url: %s", api_url)
    image_response = requests.get(api_url)
    output_path = "{}{}.jpeg".format(output_path, uuid4())
    with open(output_path, 'wb') as tmpfile:
        for chunk in image_response:
            tmpfile.write(chunk)
    return open(output_path)

