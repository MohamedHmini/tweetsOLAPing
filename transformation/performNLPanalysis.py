import sys
import os
import json
from googleNLP_API import googleNLP_API
import csv
import concurrent.futures



def NLP_processing(api, optf, tw):
    csvd = [tw['id']]
    csvd.extend(api.process(tw))
    with open(optf, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerow(csvd)

def process(js,tweetspool):
    global start
    global c
    if c == 5000:
        print(tweetspool)
        c = 0
    else:
        c+=1
    try:
        tw = json.loads(js)
    except Exception as e:
        with open(errf, 'a') as err:
            err.write(f"{tweetspool},{e}\n")
    try:
        if 'id_str' in tw.keys():
            if not start and tw['id'] == 1018659967346208768: start =True
            if start: NLP_processing(api, optf, tw)
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
    global start
    global c
    c = 0
    start = False
    executeThreading()


