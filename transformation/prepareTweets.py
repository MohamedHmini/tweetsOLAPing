import os
import sys
import json
import random
import datetime
import re
import csv
# from textblob import TextBlob
# from googletrans import Translator
from UserProcessor import UserProcessor
from TweetProcessor import TweetProcesor
from RandomTweetMetricsEstimator import RandomTweetMetricsEstimator




def loadto(data, outf):
    with open(outf, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerow(data)

def load_all_meta_data(twopt,usopt):
    twittos_meta = "us_id, loc, is_protected, is_verified, lang, followers_count, friends_count, listed_count, favourites_count, statuses_count, utc_offset, time_zone, weekday, monthname, day, hour, minute, second, year, month, user_activity, user_category"
    tweets_meta = "tw_id, usr_id, favorite_count, retweet_count, reply_count, tweet_type, is_quote, source, weekday, monthname, day, hour, minute, second, year, month,is_truncated, place_type, place_name, place_full_name, country_code, country, is_possibly_sensitive, lang, has_hashtags, has_urls,has_user_mentions, has_symbols, media_type"
    loadto(twittos_meta.split(','), usopt)
    loadto(tweets_meta.split(','), twopt)

# tw_id, usr_id, favorite_count, retweet_count, reply_count, tweet_type, is_quote, source, weekday, monthname, day, hour, minute, second, year, month
# is_truncated, place_type, place_name, place_full_name, country_code, country, is_possibly_sensitive, lang, has_hashtags, has_urls,
# has_user_mentions, has_symbols, media_type
def prepareTweet(optfile, tw):
    csvtw = tp.process(tw)
    loadto(csvtw,optfile)


# us_id, loc, is_protected, is_verified, lang, followers_count, friends_count, listed_count, favourites_count, statuses_count, 
# utc_offset, time_zone, weekday, monthname, day, hour, minute, second, year, month, user_activity, user_category
def prepareUser(optfile, tw):
    csvus = up.process(tw)
    loadto(csvus,optfile)



if __name__ == '__main__':
    args = sys.argv
    srcdir = os.path.abspath(args[1])
    twopt = os.path.abspath(args[2])
    usopt = os.path.abspath(args[3])
    errf = os.path.abspath(args[4])
    up = UserProcessor()
    tp = TweetProcesor(RandomTweetMetricsEstimator().process)

    load_all_meta_data(twopt,usopt)

    for tweetspool in os.listdir(srcdir):
        with open(os.path.join(srcdir,tweetspool)) as src:
            print(tweetspool)
            for js in src:
                try:
                    tw = json.loads(js)
                except Exception as e:
                    with open(errf, 'a') as err:
                        err.write(f"{tweetspool},{e}\n")
                try:
                    if 'id_str' in tw.keys():
                        prepareTweet(twopt, tw)
                        prepareUser(usopt, tw)
                except Exception as e:
                    with open(errf, 'a') as err:
                        err.write(f"{tw['id']},{e}\n")

