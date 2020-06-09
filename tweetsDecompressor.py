import sys
import os
import bz2




args = sys.argv
srcdir = os.path.abspath(args[1])
optdir = os.path.abspath(args[2])


try:
    os.mkdir(optdir)
except:
    pass

err = os.path.abspath("decerr.txt")
dec = bz2.BZ2Decompressor()

for f in os.listdir(srcdir):
    try:
        with bz2.open(os.path.join(srcdir, f), 'rb') as bf:
            data = bf.read()
        with open(os.path.join(optdir, f"{f.split('.')[0]}.json"), 'wb') as opt:
            opt.write(dec.decompress(data.decode('unicode_escape')))
    except Exception as e:
        print(e)
        with open(err, 'a') as errf:
            errf.write(f"{f}\n")
        pass
