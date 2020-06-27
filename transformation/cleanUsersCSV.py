import sys
import os
import csv
import codecs
import concurrent.futures





args = sys.argv
srcf = os.path.abspath(args[1])
optd = os.path.abspath(args[2])

usrsdict = {}

with open(srcf, newline='') as usrsfile:
    usrs = csv.reader(usrsfile, delimiter=',')
    c = 1
    for usr in usrs:
        d = [c, sum([int(i) for i in usr[5:10]])]
        if usr[0] in usrsdict.keys():
            usrsdict[usr[0]].append(d)
        else:
            usrsdict[usr[0]] = [d]
        c+=1


chosenusrs = [
    max(instances, key = lambda usr: usr[1])[0]
    for uid, instances
    in usrsdict.items()
]


def process(f, usr):
    with open(f, 'a', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerow(usr)

try:
    os.mkdir(os.path.abspath(optd))
except:
    pass

with concurrent.futures.ThreadPoolExecutor(20) as ex:
    with open(srcf, newline='') as usrsfile:
        usrs = csv.reader(usrsfile, delimiter=',')
        c = 1
        f = 0
        for usr in usrs:
            if f == 10:
                f = 0
            if c in chosenusrs:
                ex.submit(lambda args:process(*args), [os.path.join(optd, f"{f}.csv"),usr])
                f += 1
            c+=1
