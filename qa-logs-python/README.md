# QA Logs Python

## About
This project is meant to compare URLs that web archive playback software, such
as pywb, loads (or attempts to load) in rendering a page against a Heritrix
crawl.log file. The intention is to determine URLs that went unintentionally
uncaptured and should be added to a future crawl. The project makes use of
[pywb](https://github.com/webrecorder/pywb) to render archived pages and [webrender-puppeteer](https://github.com/ukwa/webrender-puppeteer) to generate
HAR files.

The following instructions assume you have docker and docker-compose
installed.

## Generating .har files

To run an instance of pywb in Docker where pages can be rendered via
webrender-puppeteer, from within the `qa-logs-python` directory run:

```
$ pip install docker-compose
$ docker-compose up -d
```

Initialize the collection in pywb that you want to do QA upon by running
`init_webarchive.sh` and specifying the WARC file(s) you want to include.
The following copies the WARC files at the specified path into the pywb
collection at webarchive/collections/qa-test/archive/ and indexes them to
webarchive/collections/qa-test/indexes/index.cdxj:

```
$ ./init_webarchive.sh "/tmp/warcs/*"
```

At this point, you should be able to navigate to http://localhost:8080/ in your
browser and see the qa-test collection listed. To auto-generate a .har file of
the proxy-mode playback version of a URL archived in your pywb collection, run
fetch_har.sh, specifying a file with a list of URLs you want to render:

```
$ ./fetch_har.sh seeds.txt
```

If in addition to HAR files you want to create screenshots for the archived URLs,
supply the "extended" argument also:

```
$ ./fetch_har.sh seeds.txt extended
```

After creating the derivatives, the files will be in the `/rendered` directory.

To parse the crawl logs affiliated with the WARCs in your collecion and store
their data in parquet format on disk run:

```
$ python  crawl_log_parse.py --job parse-crawl --crawl-log "/tmp/crawl_logs/*" --output-dir parquet
```

After the above sample command, parquet files are then found in the directory
`spark-warehouse/parquet`.

To combine HAR file data and crawl log file data (reading from the parquet
files) into a single data structure run:
```
$ python  crawl_log_parse.py --job add-har --har-file "rendered/*" --parquet-file spark-warehouse/parquet/
```

## crawl_log_parse.py

### Python Requirements

crawl_log_parse.py requires Python 3 and the following requirements:
  * pyspark

You can install the requirements with:
```
$ pip install -r requirements.txt
```

### Usage

### Running

Currently crawl_log_parse.py can be run with one of 3 commands: `parse-crawl`,
`add-har`, and `all`.

* `parse_crawl`: Parse lines of crawl log file(s) into a data frame stored as
parquet files. 
* `add-har`: Incorporate crawl log data into a list of entries from .har file(s)
* `all`: Run all other implemented commands.
