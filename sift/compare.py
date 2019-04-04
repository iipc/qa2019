import argparse
import json
import sys
from argparse import RawTextHelpFormatter
import importlib
import logging

with open('example_input.json') as example_file:
    example_json = example_file.read()

parser = argparse.ArgumentParser(description='Compare the original and archived versions of a URL.', 
                                 epilog='Expects an input file on stdin or specified by --input-file in the format:\n{}'.format(example_json),
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', '--input-file', dest='input_file',
                    help='a JSON input file containing entries to compare')
parser.add_argument('-o', '--output-file', dest='output_file',
                    help='a filename to which we will concatenate JSON output')

args = parser.parse_args()

input_json = json.load(args.input_file if args.input_file else sys.stdin)

output = []

for entry in input_json:
    logging.info('working on entry with id "%s"', entry.get('id'))
    original = entry.get('original', {})
    input_module = original.get('input_module')
    input_module = importlib.import_module('input.{}'.format(input_module))
    logging.info('imported "%s" to read original version',  input_module)
    original_file = input_module.fetch(original.get('url'), **original.get("additional_arguments", {}))
    
    archived = entry.get('archived', {})
    input_module = archived.get('input_module')
    input_module = importlib.import_module('input.{}'.format(input_module))
    logging.info('imported "%s" to read archived version',  input_module)
    archived_file = input_module.fetch(archived.get('url'), **archived.get("additional_arguments", {}))

    comparison_modules = entry.get('comparison_modules')
    comparison_results = []
    for comparison_item in comparison_modules:
        comparison_result = {}
        logging.info('comparing %s and %s via %s:', original_file, archived_file, comparison_item)
        comparison_module = "comparison.{}".format(comparison_item)
        comparison_result['module'] = comparison_module
        comparison_module = importlib.import_module(comparison_module)
        comparison_result['short_name'] = comparison_item
        comparison_result['name'] = comparison_module.__doc__.split("\n")[0]
        comparison_result['score'], comparison_result['metadata'] = comparison_module.compare(original_file, archived_file)
        comparison_results.append(comparison_result)
    output_dict = { 
            'id': entry.get('id'),
            'metadata': entry.get('metadata'),
            'comparison_results': comparison_results,
            }
    output.append(output_dict)

json.dump(output, open(args.output_file, 'w+') if args.output_file else sys.stdout)
