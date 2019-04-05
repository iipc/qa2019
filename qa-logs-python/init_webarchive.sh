#!/usr/bin/bash
docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager init qa-test

# move or symlink WARC files?

# reindex 
docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager reindex qa-test