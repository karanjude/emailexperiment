import sys

f = open(sys.argv[1])
f1 = open(sys.argv[2])

l_map = {}
for l in f1:
    l = l.strip()
    p = l.split()
    l_map[int(p[1])] = p[0]
f1.close()

c = 0
for l in f:
    l = l.strip()
    l = l.replace("+","")
    l = l.replace("*","")
    if c == 0:
        c += 1
        continue

    if len(l) == 0:
        continue
    p = l.split()

    r = []

    real_label = l_map[int(p[1].split(":")[0])-1]

    p = p[3:]
    n = len(p)
    for i in range(0,n):
        r.append((l_map[i],float(p[i])))
    r = sorted(r,key=lambda x:x[1],reverse = True)
    r = r[0:10]
    r = map(lambda x:x[0],r)
    print real_label, " ".join(r)

f.close()
