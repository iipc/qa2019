import json
import csv

targets = json.load(open("2019-04-03-w3act-target-list-target-list.json"))

with open('target-qa-dataset.csv', 'w') as csvfile:
    cw = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    cw.writerow(["Target ID", "Title", "Live Site Status", "QA Result", "QA Issue - Content", "QA Issue - Appearence", "QA Issue - Functionality", "Open Access", "Primary URL", "Other URLs"])
    for t in targets:
        # Skip hidden records:
        if t['field_hidden'] == True:
            continue
        # Get the QA status"
        qaIssue = None
        if t['qaIssue']:
            qaIssue = t['qaIssue']['name']
        # Only emit records where the QA status is set:
        if qaIssue and qaIssue != 'Unknown':
            urls = []
            purl = ""
            for url in t['fieldUrls']:
                if url['position'] == 0:
                    purl = url['url']
                else:
                    urls.append(url['url'])
            flags = []
            for f in t['flags']:
                if f['name'].startswith('QA'):
                  flags.append(f['name'])
            qac = 'QA Issue - Content' in flags
            qaa = 'QA Issue - Appearence' in flags
            qaf = 'QA Issue - Functionality' in flags
            cw.writerow([t['id'], t['title'], t['field_live_site_status'], qaIssue, qac, qaa, qaf, t['hasOpenAccessLicense'], purl, urls])
  

