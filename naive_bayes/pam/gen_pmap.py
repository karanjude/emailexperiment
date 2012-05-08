import sys
import os
import pickle

f = open(sys.argv[1])
p_map = {}
c_map = {}
topic_count_map = {}

def process(l):
    l = l.replace(",","")
    p = l.split()
    label = p[1]
    pl = label.split("/")
    n = len(pl)
    label = pl[n-2]

    if label not in p_map:
        p_map[label] = {}

    if label not in c_map:
        c_map[label] = 0
    c_map[label] += 1

    #print label
    n = len(p[2:])
    c = 0
    for i in range(2,n,2):
        topic_id = p[i]
        topic_prob = float(p[i+1])
        if topic_id not in p_map[label]:
            p_map[label][topic_id] = 0
        #print "topic_id >>> ", topic_id
        p_map[label][topic_id] += int(topic_prob * 100)
        if topic_id not in topic_count_map:
            topic_count_map[topic_id] = 0
        #print "topic_id >>> ", topic_id
        topic_count_map[topic_id] += int(topic_prob * 100)
        c += 1
    return c

c = 0
for l in f:
    if c == 0:
        c += 1
        continue

    l = l.strip()
    process(l)
    #print 

total_count = 0
for k,v in c_map.iteritems():
    total_count += v

t_map = {}

#print p_map

for k,v in p_map.iteritems():
    #print ">>>", k , c_map[k]
    s = 0
    for kk,vv in v.iteritems():
        prob_topic_given_label = float(vv) / (100 * float(c_map[k]))
        #print "prob_topic_%s_given_label_%s" % (kk,k) , " : " , prob_topic_given_label
        prob_label = float(c_map[k]) / float(total_count)
        #print "prob_label_%s" % (k) , " : " , prob_label
        prob_topic = float(topic_count_map[kk]) / float(total_count * 100)
        #print "prob_topic_%s" % (kk) , " : ", prob_topic
        prob_label_given_topic = float(prob_topic_given_label * prob_label) / float(prob_topic)
        #print "prob_of_label_%s_given_topic_%s" % (k,kk), " : ", prob_label_given_topic
        #print kk, vv * doc_prb 
        if kk not in t_map:
            t_map[kk] = {}
        if k not in t_map[kk]:
            t_map[kk][k] = 0

        t_map[kk][k] = prob_label_given_topic
    #print s

#for k,v in t_map.iteritems():

#    print k, v
f.close()

user_name = sys.argv[1].split(".")[0]
s_file = open(user_name + ".pmap","wb")
pickle.dump(t_map, s_file)
s_file.close()

s_file = open(user_name + ".pmap","rb")
m = pickle.load(s_file)
s_file.close()

#print m



