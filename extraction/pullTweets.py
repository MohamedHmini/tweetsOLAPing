import sys
import os
import tweepy


def getAPI(
    apikey,
    apikey_secret,
    accesstoken,
    accesstoken_secret
):
    auth = tweepy.OAuthHandler(apikey, apikey_secret)
    auth.set_access_token(accesstoken, accesstoken_secret)
    api = tweepy.API(auth)
    return api


def lookupStatuses(api, ids, path):
    tweets = api.statuses_lookup(ids)
    jstweets = [str(tw._json) for tw in tweets]
    data = str.join('\n', jstweets)
    with open(path,'a') as opt:
        opt.write(data)


args = sys.argv
srcf = os.path.abspath(args[1])
optf = os.path.abspath(args[2])
api = getAPI(
    args[3],
    args[4],
    args[5],
    args[6]
)

with open(srcf) as src:
    c = 0
    ids = []
    for tw in src:
        if tw != '\n':
            if c<100:
                ids.append(tw.split('\n')[0])
                c+=1
            else:
                lookupStatuses(api,ids,optf)
                c=0
                ids = []
    if len(ids) > 0:
        lookupStatuses(api,ids,optf)



