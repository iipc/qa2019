#!/usr/bin/env python

import csv
import argparse
import json
import sys
import pprint


parser = argparse.ArgumentParser(description='Converting the old JSON format of PROMISE to the new format of SAQA.')
parser.add_argument('-i', '--input-file', dest='input_file',
                    help='a CSV input file containing data to convert to JSON')
parser.add_argument('-o', '--output-file', dest='output_file',
                    help='a filename to which we will concatenate JSON output')

args = parser.parse_args()

output = []
id = 1
with open(args.input_file, 'r') as input_file:
    csv_reader = csv.DictReader(input_file)
    for row in csv_reader:
        output.append({
            "id": id,
            "metadata": {
                "url": row['url']
            },
            "original": {
                "input_module": "sha1",
                "url": row['url'],
                "additional_arguments": {"local_path": "/home/manu/projets/promise/explorations/screenshots_qc",
                                         "archived": False}
            },
            "archived": {
                "input_module": "sha1",
                "url": row['url'],
                "additional_arguments": {"local_path": "/home/manu/projets/promise/explorations/screenshots_qc",
                                         "archived": True}
            },
            "comparison_modules": ["ssim", "mse", "sad", "phash"]
        })
        id += 1


json.dump(output, open(args.output_file, 'w+') if args.output_file else sys.stdout)
