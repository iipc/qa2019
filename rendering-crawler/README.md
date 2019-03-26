Capturing a web page using the browser
======================================

This is an example of capturing a single web page using a browser and warcprox, that runs under Docker.

First, get warcprox running:

    cd warcprox
    docker-compose up -d

Then, you can change back to this directory and run, for example:

    ./run-renderer-capture.sh https://www.wikipedia.org/

The rendering process will log some information during the process, and afterwards the rendered images etc. will be in `./rendered/` and the WARC capture of the browser activity will be in `./warcs/`. The images are not automatically packaged into the WARCs in this setup. We use the `webrender-api` service to run the captures in production, and it stores the images.

See https://github.com/ukwa/webrender-puppeteer to understand what the renderer is doing.

----
If you do not have docker-compose installed locally, read the simple instructions at https://docs.docker.com/compose/install/ - basically you just need to download a binary.
