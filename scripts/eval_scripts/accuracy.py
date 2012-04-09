import sys

fn = sys.argv[1]
f = open(fn)
c = 0
r = 0
for l in f:
    l = l.strip()
    p = l.split()
    r += float(p[1])
    c += 1

rr = float(r) / float(c)
print "Accuracy on ", c , " items ", rr
