import os
import sys
import pickle

test_doc_topics = sys.argv[1]
user_map = sys.argv[2]

s_file = open(user_map,"rb")
label_given_t_map = pickle.load(s_file)
s_file.close()

labels = label_given_t_map[label_given_t_map.keys()[0]].keys()
#print labels

def gen_classes(real_label, prob_topic_given_doc_map):
    predicted_labels = []
    for label in labels:
        r = 0
        for topic_id,topic_prob_given_doc in prob_topic_given_doc_map.iteritems():
            if label in label_given_t_map[topic_id]:
                r += label_given_t_map[topic_id][label] * topic_prob_given_doc
        predicted_labels.append((label,r))
    predicted_labels = sorted(predicted_labels, key= lambda x:x[1], reverse=True)
    predicted_labels = predicted_labels[:10]
    predicted_labels = map(lambda x: x[0], predicted_labels)
    print real_label , " ".join(predicted_labels)

#for k,v in label_given_t_map.iteritems():
#    print k, len(v.keys())

#def gen_classes(real_label, 

def label_name(l):
    p = l.split("/")
    n = len(p)
    return p[n-2]


def process(p):
    n = len(p)
    r = {}
    for i in range(0,n,2):
        topic_id = p[i]
        topic_prob = float(p[i+1])
        r[topic_id] = topic_prob
    return r

f = open(test_doc_topics)
c = 0
for l in f:
    if c == 0:
        c += 1
        continue

    l = l.strip()
    p = l.split()
    label = label_name(p[1])
    t_given_doc = process(p[2:])

    gen_classes(label, t_given_doc)

f.close()
