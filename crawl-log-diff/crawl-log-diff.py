import sys
import os
import argparse
import tldextract
import re

def strip_url(url):
   url = url.replace('https://','')
   url = url.replace('http://','')
   if url[:4] == 'www.':
       url = url[4:]
   url = re.sub('/.*','', url)
   return url

parser = argparse.ArgumentParser()
fgroup = parser.add_mutually_exclusive_group(required=True)
fgroup.add_argument('-f', '--files',help='add at least 2 filenames, space separated; first should be the newest one that will be judged', nargs='*')
fgroup.add_argument('-j', '--jobdir',help='add H3ritrix job dir to look for log files; at least 2 launches must be present; specify --limit if wanted')
sgroup = parser.add_mutually_exclusive_group(required=False)

sgroup.add_argument('-s', '--seeds',help='specify seeds (space separated) or a seed list files (line by line)', nargs='+')
sgroup.add_argument('-d', '--dnsseeds',help='Extract seeds from DNS.',action='store_true')

parser.add_argument('-l', '--limit',help='limit the number of files processed. Must be at least 2 if set. Newest ones will be taken in first order')
parser.add_argument('-o', '--output',help='under construction: how detailed and/or what format the output should look like "talkative"',default='normal')

args = parser.parse_args()

# list of log files
logfiles = []

# get log files from command line
if args.files:
    logfiles = args.files
# get job dir from command line and log files from job dir
elif args.jobdir:
    if not os.path.isdir(args.jobdir):
        print("dir not found: '" + args.jobdir + "'")
        sys.exit()
    for launchdir in os.listdir(args.jobdir):
        if not os.path.isdir(args.jobdir + '/' + launchdir) or not launchdir.isdigit():
            continue

        lfile = args.jobdir + '/' + launchdir + '/logs/crawl.log'
        if not os.path.isfile(lfile):
            print() ('file not found: ' + lfile)
            continue

        logfiles.append(lfile)
    # let's sort descending
    logfiles.sort(reverse=True)
else:
    parser.print_help(sys.stderr)
    sys.exit();

if (len(logfiles) < 2):
    print('There must be at least 2 log files!')
    sys.exit()

# limit if set
if args.limit:
    if int(args.limit) < 2:
        print('Limit must be at least 2 if set!')
        sys.exit()
    logfiles = logfiles[:int(args.limit)]

seeds = []
if args.seeds:
    for seed in args.seeds:
        if os.path.isfile(seed):
            with open(seed) as sf:
                lines = sf.readlines()
                for line in lines:
                    seeds.append(line.strip())
        else:
            seeds.append(seed)

if args.output == 'talkative' and len(seeds)>0:
    print("SEEDS")
    print(seeds)

i = 0
stats=[]
newstats={}
oldstats={}
oldstatssums={}

# put status codes' statistics to list (each file to separate dict)
for logfile in logfiles:
    if not os.path.isfile(logfile):
        print("file not found: '" + logfile + "'")
        sys.exit()

    stats.append({})
    # create a dummy 'all' seed if seeds not wanted
    if not args.seeds:
        stats[i]['all']={}

    if args.output == 'talkative':
        print("analyzing file '" + logfile + "'")
    with open(logfile) as f:
        lines = f.readlines()
        for line in lines:
#            print() line
            row = line.split()
            if strip_url(row[3]).startswith("dns:") and not args.dnsseeds:
               continue

            if not args.seeds and not args.dnsseeds:
                stats[i]['all']['total'] = stats[i]['all'].get('total', 0) + 1
                stats[i]['all'][row[1]] = stats[i]['all'].get(row[1], 0) + 1
                continue

            if args.dnsseeds:
                # seeds needed to extract from dns records if possible
                if row[3][:4] == 'dns:':
                    seeds.append(row[3][4:])

            for seed in seeds:
                seed = strip_url(seed)
                if (strip_url(row[3]).find(seed) != -1):
                    l = tldextract.extract(row[3])

                    if seed in l.domain + '.' + l.suffix:
                        if seed not in stats[i]:
                            stats[i][seed] = {}

                        stats[i][seed]['total'] = stats[i][seed].get('total', 0) + 1
                        stats[i][seed][row[1]] = stats[i][seed].get(row[1], 0) + 1
                        continue

    i += 1

if not args.seeds and not args.dnsseeds:
    seeds.append('all')

if args.output == 'talkative':
    print(stats)

# separate new file's stats from olds
for i in range(len(stats)):
    if i == 0:
        newstats = stats[i]
    elif len(stats) < 3:
        oldstats = stats[i]
    else:
        #merge stats files together
         for seed,status in stats[i].items():
             for code,value in status.items():
                if seed not in oldstatssums:
                    oldstatssums[seed] = {}
                oldstatssums[seed][code] = oldstatssums[seed].get(code, 0) + float(value)

if args.output == 'talkative' and len(oldstatssums) > 0:
    print()
    print("Previous stats SUMs")
    print(oldstatssums)



# calculate average of olds if needed
if len(stats) > 2:
    for seed, status in oldstatssums.items():
        for code, value in status.items():
            if seed not in oldstats:
                oldstats[seed] = {}
            oldstats[seed][code] = float(value)/(len(stats)-1)

if args.output == 'talkative':
    print
    print('Latest Log file')
    print(newstats)
    print("\n")
    # print(oldstatssums)
    print('Previous files averages')
    print(oldstats)

    print("\n")


print('RESULTS')
print('-----------------------------------')
for seed,status in oldstats.items():
    print(seed)
    for code,value in status.items():
        if seed in newstats and code in newstats[seed]:
           newval = newstats[seed][code];
           res = float(newval)/float(value)
           print(code + ':' + ("%.2f" % res) + ':' + str(newval) + ':' + str(value))
        else:
            res = float(0)
            newval = 0
        if code.isdigit():
            c = int(code)
        else:
            c = 0

        if (c >=200 and c < 300 and res < 0.9) or (c >= 400 and c < 500 and res > 1.5):
            print('WARNING! ' + code + ':' + ("%.2f" % res) + ' ('+ str(newval) +' of '+ str(value) +')')
        else:
            print('OK! ' + code + ':' + ("%.2f" % res) + ' (' + str(newval) + ' of ' + str(value) + ')')

    print("\n")
