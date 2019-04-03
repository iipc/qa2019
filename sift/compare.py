import argparse
import json

parser = argparse.ArgumentParser(description='Compare the original and archived versions of a URL')
parser.add_argument('-i', '--input-file', dest='input_file',
                    help='a JSON input file containing entries to compare')

args = parser.parse_args()

input_json = json.load(arg.input_file)

for entry in input_json:
    module = __import__(module_name)
    file_a = entry.input_module
