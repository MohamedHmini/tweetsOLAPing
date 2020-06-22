import sys
import os
import csv
import codecs





args = sys.argv
srcf = os.path.abspath(args[1])
optf = os.path.abspath(args[2])

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

chosenusrs = {
    max(instances, key = lambda usr: usr[1])[0]
    for uid, instances
    in usrsdict.items()
}


with open(srcf, newline='') as usrsfile:
    usrs = csv.reader(usrsfile, delimiter=',')
    c = 1
    for usr in usrs:
        if c in chosenusrs:
            with open(optf, 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
                writer.writerow(usr)
        c+=1


