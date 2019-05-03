#!/usr/bin/env bash
docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager init qa-test

# move or symlink WARC files?
cp $1 $PWD/webarchive/collections/qa-test/archive/

# reindex 
docker run --rm -v $PWD/webarchive:/webarchive webrecorder/pywb wb-manager reindex qa-test
