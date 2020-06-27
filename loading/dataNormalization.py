import sys
import os
import csv
import concurrent.futures



def loadto(data, srcf):
    with open(srcf, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data)


def processTwittos(usr, counter, outd):
    usr[11] = usr[11].replace(',',' ')
    date_table = usr[12:15] + usr[18:20]
    timestamp_table = usr[15:18]
    location_table = usr[10:12]
    twitto_md = usr[4:5] + usr[20:22]
    twitto = usr[0:1] + usr[2:4] + usr[5:10]

    loadto([counter] + twitto, os.path.join(outd, 'twittos.csv'))
    loadto([counter] + twitto_md, os.path.join(outd, 'twitto_md.csv'))
    loadto([counter] + date_table, os.path.join(outd, 'date.csv'))
    loadto([counter] + timestamp_table, os.path.join(outd, 'timestamp.csv'))
    loadto([counter] + location_table, os.path.join(outd, 'location.csv'))


# us_id, loc, is_protected, is_verified, lang, followers_count, friends_count, listed_count, favourites_count, statuses_count, 
# utc_offset, time_zone, weekday, monthname, day, hour, minute, second, year, month, user_activity, user_category
def normalizeTwittos(srcf, outd):
    counter = 2061787
    with open(srcf, newline='') as f:
        usrs = csv.reader(f, delimiter=',')
        
        with concurrent.futures.ThreadPoolExecutor(10) as ex:
            for usr in usrs:
                ex.submit(lambda args:processTwittos(*args), [usr,counter if counter != 0 else 'id',outd])
                counter += 1

    return counter


def processTweets(tw,counter,outd):
    strs = [7] + list(range(17,22))
    for s in strs:
        tw[s] = tw[s].replace(',',' ')
    tweet = tw[0:5]
    tweet_md = tw[0:1] + tw[5:8] + tw[16:17] + tw[22:]
    date = tw[8:11] + tw[14:16]
    timestamp = tw[11:14]
    location = tw[17:22]

    loadto([counter] + tweet, os.path.join(outd, 'tweets.csv'))
    loadto([counter] + tweet_md, os.path.join(outd, 'tweet_md.csv'))
    loadto([counter] + date, os.path.join(outd, 'tweet_date.csv'))
    loadto([counter] + timestamp, os.path.join(outd, 'tweet_timestamp.csv'))
    loadto([counter] + location, os.path.join(outd, 'tweet_location.csv'))


# tw_id, usr_id, favorite_count, retweet_count, reply_count, tweet_type, is_quote, source, weekday, monthname, day, hour, minute, second, year, month
# is_truncated, place_type, place_name, place_full_name, country_code, country, is_possibly_sensitive, lang, has_hashtags, has_urls,
# has_user_mentions, has_symbols, media_type
def normalizeTweets(srcf, outd, startid):
    counter = startid
    with open(srcf, newline='') as f:
        tweets = csv.reader(f, delimiter=',')
        with concurrent.futures.ThreadPoolExecutor(10) as ex:
            for tw in tweets:
                ex.submit(lambda args:processTweets(*args), [tw,counter if counter != startid else 'id',outd])
                counter += 1


if __name__ == '__main__':
    args = sys.argv
    usf = os.path.abspath(args[1])
    twf = os.path.abspath(args[2])
    outd = os.path.abspath(args[3])

    try:
        os.mkdir(outd)
    except:
        pass

    lastid = normalizeTwittos(usf, outd)
    # normalizeTweets(twf, outd, lastid)
