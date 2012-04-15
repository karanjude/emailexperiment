import sys
import math
import MySQLdb

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()

words_file = sys.argv[5]
word_map = {}
topic_word_map = {}
doc_index = {}
doc_topics_map = {}
word_topic_map = {}

train = sys.argv[1]
doc_topics_file = sys.argv[2]
topic_words = sys.argv[3]
t_file = sys.argv[4]

def load_word_map(ff):
    f = open(ff)
    for l in f:
        l = l.strip()
        p = l.split()
        if len(p) < 2:
            continue
        word = p[0]
        word_index = int(p[1])
        word_map[word_index] = word
    
    f.close()

def load_doc_index(train):
    i = 0
    f = open(train)
    for l in f:
        l = l.strip()
        doc_index[i] = l
        i += 1
    f.close()

def load_doc_topics(doc_topics_file):
    f = open(doc_topics_file)
    d_index = 0
    for l in f:
        l = l.strip()
        p = l.split()
        label = doc_index[d_index]
        doc_label = label.split("/")[1]

        for pp in p:
            pp = pp.split(":")
            word_id = int(pp[0])
            t_c = int(pp[1])

            word = word_map[word_id] 

            if word in word_topic_map[t_c]:
                if word not in doc_topics_map:
                    doc_topics_map[word] = {}
                    
                if doc_label not in doc_topics_map[word]:
                    doc_topics_map[word][doc_label] = 0

                doc_topics_map[word][doc_label] += 1

        d_index += 1
    f.close()

def load_word_topic_probabilities(topic_words):
    f = open(topic_words)
    t_c = -1
    for l in f:
        l = l.strip()
        if l.startswith("Topic"):
            t_c += 1
            continue
        p = l.split()
        word = p[0]
        pr = float(p[1])

        if t_c not in word_topic_map:
            word_topic_map[t_c] = {}

        word_topic_map[t_c][word] = pr
    
    f.close()

def get_text(doc_id):
    #print doc_id
    c.execute("select * from doc_frequency where doc_id = %s ", (doc_id))
    rr = []
    for r in c:
        rr.append(r[1])
        
    #print rr
    return rr

def labels_for_test_file(fname):
    doc_id = fname
    actual_label = doc_id.split("/")[1]
    text = get_text(doc_id)
    r = {}

    for word in text:
        if word not in doc_topics_map:
            continue

        if len(r.keys()) == 0:
            r = doc_topics_map[word]
        else:
            v = doc_topics_map[word]
            for k,vv in v.iteritems():
                if k in r:
                    r[k] += vv

        v = r.iteritems()
        v = sorted(v, key=lambda x:x[1], reverse = True)
        v = v[0:1]

        r = {}
        for i in v:
            r[i[0]] = i[1]

    predicted_label = ""
    for k,v in r.iteritems():
        predicted_label = k
    print actual_label , predicted_label

load_word_map(words_file)
load_doc_index(train)
load_word_topic_probabilities(topic_words)
load_doc_topics(doc_topics_file)

for k,v in doc_index.iteritems():
    labels_for_test_file(v)


db.close()
