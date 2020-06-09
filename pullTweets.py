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


def lookupStatuses(api, ids):
    api.statuses_lookup(ids)
