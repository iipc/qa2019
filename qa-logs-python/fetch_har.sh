#!/bin/sh
docker run -i --rm --cap-add=SYS_ADMIN \
--network qa-logs-python_pywb-puppet --env-file env.render \
-v $PWD/rendered:/output \
-v $PWD/puppeteer-har.js:/puppeteer-har.js \
-v $PWD/renderer.js:/renderer.js \
--name puppeteer-chrome ukwa/webrender-puppeteer node renderer.js $1