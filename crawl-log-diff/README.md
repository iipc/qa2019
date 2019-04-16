**Under construction!!!**

Tool for comparing 2 or more Heritrix Crawl Log files, meant to to detect issues (e.g. abnormal differences in statistics) in frequent crawls of same seeds.

```
usage: crawl-log-diff.py [-h] (-f [FILES [FILES ...]] | -j JOBDIR)
                         [-s SEEDS [SEEDS ...] | -d] [-l LIMIT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -f [FILES [FILES ...]], --files [FILES [FILES ...]]
                        add at least 2 filenames, space separated; first
                        should be the newest one that will be judged
  -j JOBDIR, --jobdir JOBDIR
                        add H3ritrix job dir to look for log files; at least 2
                        launches must be present; specify --limit if wanted
  -s SEEDS [SEEDS ...], --seeds SEEDS [SEEDS ...]
                        specify seeds (space separated) or a seed list files
                        (line by line)
  -d, --dnsseeds        Extract seeds from DNS.
  -l LIMIT, --limit LIMIT
                        limit the number of files processed. Must be at least
                        2 if set. Newest ones will be taken in first order
  -o OUTPUT, --output OUTPUT
                        under construction: how detailed and/or what format
```

**Examples**

python crawl-log-diff.py -f job1b-crawl.log job1a-crawl.log -s atlantico.fr
RESULTS
-----------------------------------
atlantico.fr
200:0.07:119:1590
WARNING! 200:0.07 (119 of 1590)
301:0.01:1:116
OK! 301:0.01 (1 of 116)
404:0.05:5:95
OK! 404:0.05 (5 of 95)
total:0.07:128:1806
OK! total:0.07 (128 of 1806)
OK! 503:0.00 (0 of 3)
OK! 500:0.00 (0 of 2)

python crawl-log-diff.py -f job1b-crawl.log job1a-crawl.log -s bienpublic.com
RESULTS
-----------------------------------
bienpublic.com
200:0.94:3287:3481
OK! 200:0.94 (3287 of 3481)
302:1.00:5:5
OK! 302:1.00 (5 of 5)
total:0.95:3361:3536
OK! total:0.95 (3361 of 3536)
404:1.68:47:28
WARNING! 404:1.68 (47 of 28)
301:1.00:22:22
OK! 301:1.00 (22 of 22)
