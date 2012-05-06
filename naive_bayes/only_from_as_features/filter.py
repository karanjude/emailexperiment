import sys

f = open(sys.argv[1])

for l in f:
    l = l.strip()
    p = l.split()

    tag = p[0]
    tag = tag.split('/')
    n1 = len(tag)
    label = tag[n1-2]    
    
    p = p[1:]
    n = len(p)
    r = []
    for i in range(0,n,2):
        tag = p[i]
        prob = float(p[i+1])
        r.append((tag,prob))
        #tag = tag.split("/")[1]

    r = sorted(r, key=lambda x:x[1], reverse=True)
    r = map(lambda x:x[0], r)

    r = r[:10]
    print label , " ".join(r)



f.close()
