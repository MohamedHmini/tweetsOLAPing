import sys
import os
import random
import json
import re



def randomSelector(fpath):
    m = set()
    try:
        with open(fpath) as tweetspool:
            for tweet in tweetspool:
                js = json.loads(tweet)
                if "id_str" in js.keys(): 
                    m.add(js['user']['utc_offset'])
    except:
        pass
    return m
        

args = sys.argv
srcdir = os.path.abspath(args[1])
m = set()
for tweetspool in os.listdir(srcdir):
    m = m.union(randomSelector(os.path.join(srcdir, tweetspool)))
    print(m)



# def detectLanguage(t, tx):
#     lng = t.detect(tx)
#     return lng.lang

# def translateToEnglish(t, tx, lang):
#     entx = t.translate(tx, src = lang)
#     return entx.text

# def performSentimentAnalysis(tx):
#     pol,sub = None,None
#     polarity,subjectivity = TextBlob(tx).sentiment
#     if subjectivity > 0.5:
#         sub = 'very-positive'
#     elif 0 < subjectivity <= 0.5:
#         sub = 'positive'
#     elif subjectivity < -0.5:
#         sub = 'very-negative'
#     elif -0.5 <= subjectivity <0:
#         sub = 'negative'
#     else:
#         sub = 'neutral'
    
#     if polarity >= 0.5:
#         pol = 'subjective'
#     elif polarity < 0.5:
#         pol = 'objective'
#     return pol,sub
