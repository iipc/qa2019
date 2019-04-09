import argparse
import json
import os
import re
import sys
from glob import glob

from pyspark.sql.types import *
from pyspark.sql import SparkSession, SQLContext, functions as F


URL_EXTRACTOR = re.compile(r'(?:.*)/\d{14,}(?:[a-zA-Z]*_)?/(.*)$')


def validate_args(args):
    return True


def normalize_crawl_entry(row):
    """Produce a row with 13 fields.

    Some crawl logs have lines of varied length. They may not have the
    annotation nor JSON fields. It may not be good to assume there
    should be exactly 13 fields or that the 13th is JSON? If we don't
    need the fields past a certain number, we can do away with some
    of the logic here...Anyway, currently this currently assumes we
    want all rows to have 13 fields.
    """
    # replace all multiple whitespace instances
    # in order to more accurately split on 
    # whitespace delimiter
    row = re.sub(" +", " ", row.strip())
    # if row has 11 fields,
    # return list plus two "-"
    # to account for missing annotations
    # and json blob
    if row.count(" ") == 10:
        return row.split() + ["-", "-"]
    
    # if we're here, then row has additional fields
    row = row.split(" ", 11)

    # check for json blob
    if "{" not in row[-1]:
        row.append("-")
    else:
        # splitting the row at the space before the json blob
        # and piecing them back together with the whole row
        row = row[:-1] + [row[-1][:row[-1].index("{") - 1], row[-1][row[-1].index("{"):]]
    return row


def fetch_har_entry_pairs(har_file, no_proxy=False):
    for g in glob(har_file):
        with open(g, 'r') as f:
            har = json.loads(f.read())
            entries = []
            for e in har['log']['entries']:
                # this could be appended to a list and we return that instead.
                # not yet clear on how we want to handle this.
                #yield (e['request']['url'], e['response']['redirectURL'], e['response']['status'])
                #yield {
                url = e['request']['url']
                if no_proxy:
                    url = extract_archived_url(url)
                    if url is None:
                        continue
                entries.append({
                    'url': url,
                    'status': e['response']['status'],
                    'mime_type': e['response']['content']['mimeType'],
                    'size': e['response']['content']['size'],
                })
    return entries



def run(args):
    spark = SparkSession.builder.appName("CrawlLogs" ).getOrCreate()
    validate_args(args)

    if args.job in ["parse-crawl", "all"]:
        run_parse_crawl_job(spark, args.crawl_log, args.output_dir)
    if args.job in ["add-har", "all"]:
        print(run_add_har(spark, args.parquet_file, args.har_file, args.no_proxy))
    spark.stop()


def run_parse_crawl_job(spark, crawl_log, output_dir='parquet'):
    schema = StructType.fromJson({'fields': [
        {'metadata': {},'name': 'timestamp', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'fetch_code', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'document_size', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'downloaded_url', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'discover_path', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'referrer', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'mime_type', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'worker_thread', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'fetch_timestamp', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'digest', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'source_tag', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'annotations', 'nullable': False, 'type': 'string'},
        {'metadata': {},'name': 'json_info', 'nullable': False, 'type': 'string'}
    ], 'type': 'struct'})

    sc = spark.sparkContext
    input_data = sc.textFile(crawl_log)
    output_data = input_data.map(normalize_crawl_entry)
    df = spark.createDataFrame(output_data, schema)
    df.createOrReplaceTempView("logs")

    df.coalesce(10).write.format("parquet").saveAsTable(output_dir)


def extract_archived_url(url):
    """Remove playback app portion of URL for non-proxy replay"""
    match = URL_EXTRACTOR.match(url)
    if match:
        url = match.group(1)
    else:
        # there was no timestamp;
        # assume url is playback app's own asset etc. and skip
        return None
    return url


def run_add_har(spark, parquet_file, har_file, no_proxy=False):
    sc = spark.sparkContext
    sql_context = SQLContext(sc)
    df = sql_context.read.parquet(parquet_file)
    df.createOrReplaceTempView("logs")

    data = fetch_har_entry_pairs(har_file, no_proxy)
    urls = [x.get('url') for x in data]
    urls = set(urls)
    results = df[df.downloaded_url.isin(urls)].collect()
    # convert results to a dictionary for url lookup
    log_data = {}
    for row in results:
        # combine data base on dowloaded url; retain only some fields
        log_data.setdefault(row.downloaded_url, []).append({
            "timestamp": row.fetch_timestamp,
            "referrer": row.referrer,
            "status": row.fetch_code,
            "size": row.document_size,
            "mime_type": row.mime_type,
        })
    for dicts in data:
        # add in the crawl log data for the har entry
        dicts["log_data"] = log_data.get(dicts["url"])
    return json.dumps(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--job",
        help="Type of job to run. Options: "
        "parse-crawl, add-har, visualize, all",
        choices=["parse-crawl", "add-har", "visualize", "all"]
    )
    parser.add_argument(
        "--crawl-log",
        dest="crawl_log",
        help="Location of crawl log(s) to read from. Accepts wildcard character."
    )
    parser.add_argument(
        "--har-file",
        dest="har_file",
        help="Location of har file(s) to read from. Accepts wildcard character."
    )
    parser.add_argument(
        "--parquet-file",
        dest="parquet_file",
        help="Location of parquet file(s) to read from. Accepts wildcard character."
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        help="Directory to save output to; cannot exist."
    )
    parser.add_argument(
        "--no-proxy-mode",
        dest="no_proxy",
        action='store_true',
        help="Non proxy mode indicates archived URL should be extracted from replay URL."
    )

    args = parser.parse_args()
    run(args)
