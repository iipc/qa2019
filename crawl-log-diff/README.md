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


