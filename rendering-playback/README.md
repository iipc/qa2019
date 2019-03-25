Screenshotting during playback
==============================

Here we run Python Wayback set up so we can render archived sites in a browser.

In `pywb` folder, a suitable collection was created uaing:

    docker pull webrecorder/pywb
    docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager init qa-test

then added WARC file to `webarchive/collections/qa-test/archive/` and ran

    docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager reindex qa-test

You can add more WARCs and repeat this step to ensure they play back.

The playback service itself should be started with:

    docker-compose up -d

Then you can visit http://localhost:8080/qa-test/20190325141320/https://www.wikipedia.org/

To capture the proxy-mode playback version in the browser, you can then use:

    ./run-rendered-playback.sh https://www.wikipedia.org/

and outputs will be in the `rendered` folder.

