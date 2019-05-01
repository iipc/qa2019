# QA Logs Python

## crawl_log_parse.py

### Requirements

crawl_log_parse.py requires Python 3 and the following requirements:
  * pyspark

You can install the requirements with:
 `$ pip install -r requirements.txt`

### Running

Currently crawl_log_parse.py can be run with one of 3 commands: `parse-crawl`,
`add-har`, and `all`.

* `parse_crawl`: Parse lines of crawl log file(s) into a data frame stored as
parquet files. 
* `add-har`: Incorporate crawl log data into a list of entries from .har file(s)
* `all`: Run all other implemented commands.
