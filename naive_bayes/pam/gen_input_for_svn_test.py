import sys

user = sys.argv[1].split(".")[0]
f = open(user + ".labels")
l_map = {}
for l in f:
    l = l.strip()
    p = l.split()
    l_map[p[0]] = int(p[1])
f.close()
max_c = len(l_map.keys())

#print max_c

f = open(sys.argv[1])

c = 0
for l in f:
    if c == 0:
        c += 1
        continue

    l = l.strip()
    p = l.split()
    
    user = p[1].split("/")
    n = len(user)
    user = user[n-2]

    if user == "india" or user == "australia":
        continue
    
    p = p[2:]
    n = len(p)

    r = {}
    for i in range(0,n,2):
        tid = p[i]
        tp = float(p[i+1])
        r[tid] = tp

    
    n = len(r.keys())
    rr = []
    for i in range(0,n):
        rr.append((str(i),r[str(i)]))

    rr = ["%s:%s" % (x[0],x[1]) for x in rr]

    label = user

    if label not in l_map:
        max_c += 1
        l_map[label] = max_c

    print l_map[label] ,  " ".join(rr)

f.close()
