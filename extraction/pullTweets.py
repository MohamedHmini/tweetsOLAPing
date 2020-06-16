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
    'kp4X0DiSXOKhPeMU6yZyPEO6t',
    'c88fpnd6LtqkbzJSF3tgmAn59XlkGOFHfUdNCAan6GaJjmgbfK',
    '3743390783-YV3X5SwhSQqH7JotPOO8OEpoZl6TrBCi9TPOexR',
    'mjqei2AWi8U7JoWC3FA6Lhl6Ro5ERzjnDhQXGv3MpSsDk'
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



