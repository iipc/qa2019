#!/usr/bin/env python

import json
import csv
import pprint

with open('../computations.log.json', 'r') as input:
    urls = json.load(input)

urls_csv = []
for url in urls:
    urls_csv.append([url,
                     None,
                     urls[url]['original'].replace('screenshots/', ''),
                     urls[url]['archived'].replace('screenshots/', '')])

with open('../computations.log.csv', 'w') as output:
    url_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for url_csv in urls_csv:
        url_writer.writerow(url_csv)
