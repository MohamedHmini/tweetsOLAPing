import sys
import os




args = sys.argv
source = os.path.abspath(args[1])
trgt_dir = os.path.abspath(args[2])

try:
    os.mkdir(trgt_dir)
except:
    pass

with open(source) as urls:
    hd = True
    for url in urls:
        if not hd:
            url = url.split(',')
            root = os.path.join(trgt_dir, url[1])
            url[2] = url[2].split("\n")[0]
            f_path = os.path.join(root, f"{url[2]}.txt") 
            try:
                os.mkdir(root)
            except:
                pass
            with open(f_path, 'a') as f:
                f.write(f"{url[0]}\n")
        else:
            hd = False
        

