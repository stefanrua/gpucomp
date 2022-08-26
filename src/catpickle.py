#!/usr/bin/env python3

import pickle
import sys


merge = False
files = sys.argv[1:]

if sys.argv[1] == 'merge':
    files = sys.argv[2:]
    merge = True

d = {}
for f in files:
    p = pickle.load(open(f, 'rb'))
    d.update(p)
print(d)

if merge:
    pickle.dump(d, open('comps_merged.pkl', 'wb'))
    print('Wrote comps_merged.pkl')
