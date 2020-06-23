import sys
import os
import csv




def loadto(data, srcf):
    with open(srcf, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerow(data)


# us_id, loc, is_protected, is_verified, lang, followers_count, friends_count, listed_count, favourites_count, statuses_count, 
# utc_offset, time_zone, weekday, monthname, day, hour, minute, second, year, month, user_activity, user_category
def normalizeTwittos(srcf, outd):
    counter = 0
    with open(srcf, newline='') as f:
        usrs = csv.reader(f, delimiter=',')

        for usr in usrs:
            date_table = usr[12:15] + usr[18:20]
            timestamp_table = usr[15:18]
            location_table = usr[10:12]
            twitto_md = usr[4:5] + usr[20:22]
            twitto = usr[0:4] + usr[5:9]

            loadto([counter] + twitto, os.path.join(outd, 'twittos.csv'))
            loadto([counter] + twitto_md, os.path.join(outd, 'twitto_md.csv'))
            loadto([counter] + date_table, os.path.join(outd, 'date.csv'))
            loadto([counter] + timestamp_table, os.path.join(outd, 'timestamp.csv'))
            loadto([counter] + location_table, os.path.join(outd, 'location.csv'))
            counter += 1


# tw_id, usr_id, favorite_count, retweet_count, reply_count, tweet_type, is_quote, source, weekday, monthname, day, hour, minute, second, year, month
# is_truncated, place_type, place_name, place_full_name, country_code, country, is_possibly_sensitive, lang, has_hashtags, has_urls,
# has_user_mentions, has_symbols, media_type
def normalizeTweets(srcf, outd):
    counter = 0
    with open(srcf, newline='') as f:
        tweets = csv.reader(f, delimiter=',')

        for tw in tweets:
            tweet = tw[0:5]
            tweet_md = tw[5:8] + tw[16:17] + tw[22:]
            date = tw[8:11] + tw[14:16]
            timestamp = tw[11:14]
            location = tw[17:22]

            loadto([counter] + tweet, os.path.join(outd, 'tweets.csv'))
            loadto([counter] + tweet_md, os.path.join(outd, 'tweet_md.csv'))
            loadto([counter] + date, os.path.join(outd, 'tweet_date.csv'))
            loadto([counter] + timestamp, os.path.join(outd, 'tweet_timestamp.csv'))
            loadto([counter] + location, os.path.join(outd, 'tweet_location.csv'))
            counter += 1


if __name__ == '__main__':
    args = sys.argv
    srcf = os.path.abspath(args[1])
    outd = os.path.abspath(args[2])
    mode = int(args[3]) # 1 = twittos, 2 = tweets

    try:
        os.mkdir(outd)
    except:
        pass

    if mode == 1: normalizeTwittos(srcf, outd)
    elif mode == 2: normalizeTweets(srcf, outd)
    else: print("mode is either 1 (twittos) or 2 (tweets)")
