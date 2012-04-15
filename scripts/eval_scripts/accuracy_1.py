import sys

fn = sys.argv[1]
f = open(fn)

correct = 0
n = 0

for l in f:
    l = l.strip()
    p = l.split()
    actual = p[0]
    if len(p) > 0:
        if actual in p[1:]:
            correct += 1


    n += 1

print "total : ", n 
print "correct :", correct
r = float(correct) / float(n)
r = r * 100
print "accuracy : ", r
    
f.close()
