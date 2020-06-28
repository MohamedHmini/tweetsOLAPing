import sys
import os
import requests as req


args = sys.argv
src = os.path.abspath(args[1])
optdir = os.path.abspath(args[2])
errfile = os.path.abspath(args[3])

try:
    os.mkdir(optdir)
except:
    pass

with open(src) as srcf:
    count = 1
    for url in srcf:
        url = url.split('\n')[0][2:]
        try:
            r = req.get(f"https://{url}")
            with open(os.path.join(optdir, f"{count}.json.bz2"), 'wb') as opt:
                opt.write(r.content)
        except:
            with open(errfile, 'a') as err:
                err.write(f"{url}\n")
            pass
        count += 1
