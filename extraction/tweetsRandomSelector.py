import sys
import os
import random
import json



def randomSelector(fpath, sample_size = 200):
    tweets = []
    with open(fpath) as tweetspool:
        for tweet in tweetspool:
            js = json.loads(tweet)
            if "id_str" in js.keys(): tweets.append(js['id_str'])
    random.shuffle(tweets)
    tweets = random.sample(tweets, sample_size)
    return tweets
    
        

# try:
#     tweets.append(json.loads(tweetspool.read())['id'])
# except:
#     pass

args = sys.argv
srcdir = os.path.abspath(args[1])
optf = os.path.abspath(args[2])
sample_size = int(args[3])

for tweetspool in os.listdir(srcdir):
    tweets = randomSelector(os.path.join(srcdir, tweetspool), sample_size)
    with open(optf, 'a') as opt:
        opt.write(str.join('\n', tweets))
