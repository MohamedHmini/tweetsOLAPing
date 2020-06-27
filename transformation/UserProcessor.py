import datetime




class UserProcessor:

    def getUserCategory(self, us):
        uscat = 'information-seeker'
        usratio = us['followers_count'] / (1 + us['friends_count'])
        if usratio > 1:
            uscat = 'information_sharing'
        elif 0.8 <= usratio <= 1:
            uscat = 'friendship-relationship'
        return uscat

    def getUserActivity(self, tw):
        dc = datetime.datetime.strptime(tw['user']['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        tc = datetime.datetime.strptime(tw['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        d = (tc - dc).days
        usratio = tw['user']['statuses_count']/(1+d)
        usactivitytype = 'old' if d > 395 else 'new'
        usactivitytype += f"-{'active' if usratio >= 1 else 'passive'}"
        return usactivitytype
    
    def createdAt(self, tw):
        dc = datetime.datetime.strptime(tw['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        return [dc.strftime("%a"), dc.strftime("%b"), dc.day, dc.hour, dc.minute, dc.second, dc.year, dc.month]

    def process(self,tw):
        # us_id, loc, is_protected, is_verified, lang, followers_count, friends_count, listed_count, favourites_count, statuses_count, 
        # utc_offset, time_zone, weekday, monthname, day, hour, minute, second, year, month, user_activity, user_category
        us = tw['user']
        csvus = [us['id']]
        csvus.append(us['location'])
        csvus.append(us['protected'])
        csvus.append(us['verified'])
        csvus.append(us['lang'])
        csvus.append(us['followers_count'])
        csvus.append(us['friends_count'])
        csvus.append(us['listed_count'])
        csvus.append(us['favourites_count'])
        csvus.append(us['statuses_count'])
        csvus.append(us['utc_offset'])
        csvus.append(us['time_zone'])
        csvus.extend(self.createdAt(us))
        csvus.append(self.getUserActivity(tw))
        csvus.append(self.getUserCategory(us))
        return csvus
    

            