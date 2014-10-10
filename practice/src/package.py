import sys

print "path#################"
for p in sys.path:
    print p
print "path#################"

import test.hoge
print test.hoge
print dir(test.hoge)
for n in  dir(test.hoge):
    print n, getattr(test.hoge, n)
