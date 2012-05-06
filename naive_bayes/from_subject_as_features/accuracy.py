import sys

f = open(sys.argv[1])
n = int(sys.argv[2])

p_c = 0
t = 1

for l in f:
    l = l.strip()
    p = l.split()
    rest = p[1:]
    tag = p[0]

    for i in rest[:n]:
        if i == tag:
            p_c += 1

    t += 1
f.close()

print float(p_c)/float(t)
