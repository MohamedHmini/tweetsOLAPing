import sys
import os
import json
from googleNLP_API import googleNLP_API
import csv
import concurrent.futures


def loadto(data, optf):
    with open(optf, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerow(data)

def load_meta_data(optf):
    md = 'tw_id,sentiment_score,sentiment_magnitude,sentiment_tag,content_type'
    loadto(md.split(','),optf)

def NLP_processing(api, optf, tw):
    csvd = [tw['id']]
    csvd.extend(api.process(tw))

def process(js,tweetspool):
    try:
        tw = json.loads(js)
    except Exception as e:
        with open(errf, 'a') as err:
            err.write(f"{tweetspool},{e}\n")
    try:
        if 'id_str' in tw.keys():
            NLP_processing(api, optf, tw)
    except Exception as e:
        with open(errf, 'a') as err:
            err.write(f"{tw['id']},{e}\n")

def executeThreading():
    with concurrent.futures.ThreadPoolExecutor(3) as ex:
        for tweetspool in os.listdir(srcdir):
            with open(os.path.join(srcdir,tweetspool)) as src:
                for js in src:
                    ex.submit(lambda args:process(*args), [js,tweetspool])


if __name__ == '__main__':
    api = googleNLP_API() 
   
    args = sys.argv
    srcdir = os.path.abspath(args[1])
    optf = os.path.abspath(args[2])
    errf = os.path.abspath(args[3])

    load_meta_data(optf)
    executeThreading()


