import sys
import os
import random
import json



def randomSelector(fpath):
    ids = []
    try:
        with open(fpath) as tweetspool:
            for tweet in tweetspool:
                js = json.loads(tweet)
                if "id_str" in js.keys(): 
                    if js['user']['followers_count'] > 10000:
                        ids.append(js['id_str'])
    except:
        pass

    return ids
        

args = sys.argv
srcdir = os.path.abspath(args[1])
optf = os.path.abspath(args[2])

ids = []
for tweetspool in os.listdir(srcdir):
    ids.extend(randomSelector(os.path.join(srcdir, tweetspool)))

tweets = str.join('\n',ids)
with open(optf,'a') as opt:
    opt.write(tweets)
