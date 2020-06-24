import sys
import os



args = sys.argv
srcf = os.path.abspath(args[1])


with open(srcf, 'rb') as f:
    data = f.read()

with open(srcf, 'wb') as f:
    f.write(data)