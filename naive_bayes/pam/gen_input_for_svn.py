import sys

f = open(sys.argv[1])

label_c = 0
l_map = {}

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
    
    p = p[2:]
    n = len(p)

    if user == "australia" or user == "india":
        continue

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
        l_map[label] = label_c
        label_c += 1

    if c == 1:
        topics = []
        for i in range(0,len(rr)):
            topics.append("t" + str(i))
        
        #print str(l_map[label]) + "," + ",".join(topics) 
        c += 1

    print l_map[label] ,  " ".join(rr)

user = sys.argv[1].split(".")[0]
ff = open(user + ".labels","w")
for k,v in l_map.iteritems():
    ff.write(k + " " + str(v))
    ff.write("\n")
ff.close()


f.close()
