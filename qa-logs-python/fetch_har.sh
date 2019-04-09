#!/bin/sh
cmd="docker run -i --rm --cap-add=SYS_ADMIN 
--network qa-logs-python_pywb-puppet --env-file env.render 
-v $PWD/rendered:/output 
-v $PWD/puppeteer-har.js:/puppeteer-har.js 
-v $PWD/renderer.js:/renderer.js "
if [[ -f $1 ]]; then
    cmd="$cmd -v $PWD/$1:/$1 
    --name puppeteer-chrome ukwa/webrender-puppeteer node renderer.js $1 $2
    "
else
    cmd="$cmd --name puppeteer-chrome ukwa/webrender-puppeteer node renderer.js $1 $2
    "
fi

eval $cmd