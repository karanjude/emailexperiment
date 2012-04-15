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
labels = {}
word_label_map = {}

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
        
        if doc_label not in labels:
            labels[doc_label] = 0

        labels[doc_label] += 1

        for pp in p:
            pp = pp.split(":")
            word_id = int(pp[0])
            t_c = int(pp[1])

            word = word_map[word_id]
            if word not in word_topic_map:
                word_topic_map[word] = {}
            if t_c not in word_topic_map[word]:
                word_topic_map[word][t_c] = 0
            word_topic_map[word][t_c] += 1

            if t_c not in doc_topics_map:
                doc_topics_map[t_c] = {}

            if doc_label not in doc_topics_map[t_c]:
                doc_topics_map[t_c][doc_label] = 0

            doc_topics_map[t_c][doc_label] += 1

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

        if word not in word_topic_map:
            word_topic_map[word] = {}

        if t_c not in word_topic_map[word]:
            word_topic_map[word][t_c] = pr
    
    f.close()

def get_text(doc_id):
    #print doc_id
    c.execute("select * from doc_frequency where doc_id = %s ", (doc_id))
    rr = []
    for r in c:
        rr.append(r[1])
        
    #print rr
    return rr

def calculate_top_topics_probability():
    for k,v in doc_topics_map.iteritems():
        labels_for_topic = v
        n = 0
        for kk,vv in labels_for_topic.iteritems():
            n += vv
        for kk,vv in labels_for_topic.iteritems():
            doc_topics_map[k][kk] = float(vv)/float(n)

def labels_for_test_file(fname):
    doc_id = fname
    actual_label = doc_id.split("/")[1]
    text = get_text(doc_id)
    r = {}

    for word in text:
        if word not in word_label_map:
            continue

        if len(r.keys()) == 0:
            r = word_label_map[word]
            for k,v in r.iteritems():
                if v > 0:
                    r[k] = -math.log10(v)
                else:
                    r[k] = v
        else:
            v = word_label_map[word]
            for k,vv in v.iteritems():
                if k in r:
                    if vv > 0:
                        r[k] += -math.log10(vv)
                    else:
                        r[k] += vv

        v = r.iteritems()
        v = sorted(v, key=lambda x:x[1], reverse = True)
        v = v[0:30]

        r = {}
        for i in v:
            r[i[0]] = i[1]

    predicted_label = ""
    r = r.iteritems()
    r = sorted(r,key = lambda x:x[1],reverse = True)
    r = r[0:7]

    if len(r) > 0:
        predicted_label = r[0][0]

    print actual_label , predicted_label

def calculate_word_label_probability():
    for word,topics in word_topic_map.iteritems():
        for topic,topic_pr_given_word in topics.iteritems():
            for label, label_pr_given_topic in doc_topics_map[topic].iteritems():
                if word not in word_label_map:
                    word_label_map[word] = {}
                if label not in word_label_map[word]:
                    word_label_map[word][label] = 0
                word_label_map[word][label] += topic_pr_given_word * label_pr_given_topic

    for k,v in word_label_map.iteritems():
        labels = v.iteritems()
        labels = sorted(labels, key = lambda x:x[1],reverse = True)
        labels = labels[0:10]
        word_label_map[k] = {}
        for i in labels:
            word_label_map[k][i[0]] = i[1]

def calculate_word_topic_probabilites():
    for word,topics in word_topic_map.iteritems():
        n = 0
        for k,v in topics.iteritems():
            n += v
        for k,v in topics.iteritems():
            word_topic_map[word][k] = float(v)/float(n)

load_word_map(words_file)
load_doc_index(train)
#load_word_topic_probabilities(topic_words)
load_doc_topics(doc_topics_file)
calculate_word_topic_probabilites()
calculate_top_topics_probability()
calculate_word_label_probability()

for k,v in doc_index.iteritems():
    labels_for_test_file(v)


db.close()
