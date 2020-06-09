import sys
import os
import random

    
def randomSelector(fpath, sample_size = 2):
    urls = []
    with open(fpath) as f:
        for url in f:
            urls.append(url.split('\n')[0])
    random.shuffle(urls)
    urls = random.sample(urls, sample_size)
    urls = str.join('\n', urls)
    return urls

args = sys.argv
root = os.path.abspath(args[1])
optf = os.path.abspath(args[2])
sample_size = int(args[3])

for sub_stream in os.listdir(root):
    fld = os.path.join(root, sub_stream)
    for f in os.listdir(fld):
        urls = randomSelector(os.path.join(fld, f), sample_size)
        with open(optf, 'a') as opf_obj:
            opf_obj.write(f"{urls}\n")

