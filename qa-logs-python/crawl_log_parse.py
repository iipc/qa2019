import argparse
import json
import os
import re
import sys
from glob import glob

from pyspark.sql.types import *
from pyspark.sql import SparkSession


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
    row = re.sub(" +", " ", row)

    # if row has 11 fields,
    # return list plus two "-"
    # to account for missing annotations
    # and json blob
    if row.count(" ") == 10:
        return row.split() + ["-", "-"]
    
    # if we're here, then row has addtional fields
    row = row.split(" ", 11)

    # check for json blob
    if "{" not in row[-1]:
        row.append("-")
    else:
        # splitting the row at the space before the json blob
        # and piecing them back together with the whole row
        row = row[:-1] + [row[-1][:row[-1].index("{")], row[-1][row[-1].index("{"):]]

    return row


def fetch_har_entry_pairs(har_file):
    for g in glob(har_file):
        with open(g, 'r') as f:
            har = json.loads(f.read())
            for e in har['log']['entries']:
                # this could be appended to a list and we return that instead.
                # not yet clear on how we want to handle this.
                yield (e['request']['url'], e['response']['redirectURL'], e['response']['status'])

def run(args):
    spark = SparkSession.builder.appName("CrawlLogs" ).getOrCreate()
    validate_args(args)

    if args.job == "parse-crawl":
        run_parse_crawl_job(spark, args)
    spark.stop()


def run_parse_crawl_job(spark, args):
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
    input_data = sc.textFile(args.crawl_log)
    output_data = input_data.map(normalize_crawl_entry)
    df = spark.createDataFrame(output_data, schema)
    df.createOrReplaceTempView("logs")
    results = spark.sql("SELECT downloaded_url FROM logs")
    results.show()

#    df.coalesce()\
#        .write()\
#        .format("parquet") \
#        .saveAsTable(args.output_dir)


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
    args = parser.parse_args()
    run(args)
