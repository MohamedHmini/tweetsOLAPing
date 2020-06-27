import sys
import os




args = sys.argv
srcd = os.path.abspath(args[1])
optd = os.path.abspath(args[2])
tw_batch_size = int(args[3])
usr_batch_size = int(args[4])

try:
    os.mkdir(optd)
except:
    pass

for fn in os.listdir(srcd):
    fp = os.path.join(srcd,fn)
    if os.path.isdir(fp): continue
    op = os.path.join(optd, fn)
    c = 0
    with open(fp) as srcf:
        for l in srcf:
            if ('tw' in fn and c == tw_batch_size) or ('us' in fn and c == usr_batch_size):
                break
            with open(op, 'a') as optf:
                optf.write(l)
            c += 1




