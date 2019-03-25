In `pywb` folder. Created using:

    docker pull webrecorder/pywb
    docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager init qa-test

then added WARC file to `webarchive/collections/qa-test/archive/` and ran

    docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager reindex qa-test

then service started via

    docker-compose up -d

Then you can visit http://localhost:8080/qa-test/20190325141320/https://www.wikipedia.org/

Then

    ./run-rendered-playback.sh https://www.wikipedia.org/

and outputs will be in the `rendered` folder.

