import datetime
import re





class TweetProcesor:
    estimator = None
    
    def __init__(self, estimator = lambda tw: (tw['favorite_count'], tw['retweet_count'], tw['reply_count'] if 'reply_count' in tw.keys() else 0)):
        self.estimator = estimator

    def getTweetType(self, tw):
        tweettype = 'normal-tweet'
        if tw['in_reply_to_screen_name'] != None:
            tweettype = 'response'
        elif 'retweeted_status' in tw.keys():
            tweettype = 'retweet'
        elif len(tw['entities']['user_mentions']) > 0:
            tweettype = 'mentions'

        isquote = tw['is_quote_status']
        
        return [tweettype,isquote]

    def exctractSource(self, tw):
        p = re.compile(r"(?<=>).*(?=<)")
        return p.findall(tw['source'])[0]
        
    def getLocation(self, tw):
        # placetype, name, fullname, countrycode, country, 
        loc = [None,None,None,None,None]
        if tw['place']:
            loc[0] = tw['place']['place_type']
            loc[1] = tw['place']['name']
            loc[2] = tw['place']['full_name']
            loc[3] = tw['place']['country_code']
            loc[4] = tw['place']['country']
        return loc

    def getLanguage(self, tw):
        return tw['lang']

    def createdAt(self, tw):
        dc = datetime.datetime.strptime(tw['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        return [dc.strftime("%a"), dc.strftime("%b"), dc.day, dc.hour, dc.minute, dc.second, dc.year, dc.month]

    def getMedia(self,tw):
        mt = None
        if 'extended_entities' in tw.keys():
            if 'media' in tw['extended_entities'].keys():
                mt = tw['extended_entities']['media'][0]['type']
        return mt

    def process(self, tw):
        # tw_id, usr_id, favorite_count, retweet_count, reply_count, tweet_type, is_quote, source, weekday, monthname, day, hour, minute, second, year, month
        # is_truncated, place_type, place_name, place_full_name, country_code, country, is_possibly_sensitive, lang, has_hashtags, has_urls,
        # has_user_mentions, has_symbols, media_type
        csvtw = [tw['id'], tw['user']['id']]
        Y = self.estimator(tw)
        csvtw.extend(Y)
        csvtw.extend(self.getTweetType(tw))
        csvtw.append(self.exctractSource(tw))
        csvtw.extend(self.createdAt(tw))
        csvtw.append(tw['truncated'])
        csvtw.extend(self.getLocation(tw))
        csvtw.append(tw['possibly_sensitive'] if 'possibly_sensitive' in tw.keys() else None)
        csvtw.append(self.getLanguage(tw))
        csvtw.append(tw['entities']['hashtags'] != [])
        csvtw.append(tw['entities']['urls'] != [])
        csvtw.append(tw['entities']['user_mentions'] != [])
        csvtw.append(tw['entities']['symbols'] != [])
        csvtw.append(self.getMedia(tw))
        return csvtw
            
        