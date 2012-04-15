import sys
import math
import MySQLdb

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()

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

def load_topic_word_map(tw):
    twf = open(tw)
    t_c = 0
    for l in twf:
        c_c = 0
        l = l.strip()
        p = l.split()
        p = map(float, p)
        n = len(p)
        topic = t_c
        topic_word_map[topic] = {}
        print "processingg ", topic
        for i in range(0,n):
            word_id = i
            if word_id in word_map:
                word = word_map[word_id]
                if word not in topic_word_map[topic]:
                    topic_word_map[topic][word] = []
                topic_word_map[topic][word].append(p[i])
        t_c += 1

def load_doc_index(train):
    i = 0
    f = open(train)
    for l in f:
        l = l.strip()
        p = l.split("/")
        label = p[1]
        doc_index[i] = label
        i += 1
    f.close()

def load_doc_topics(doc_topics_file):
    f = open(doc_topics_file)
    d_index = 0
    for l in f:
        l = l.strip()
        p = l.split()
        doc_label = doc_index[d_index]

        for pp in p:
            pp = pp.split(":")
            word_id = pp[0]
            t_c = int(pp[1])

            if t_c not in doc_topics_map:
                doc_topics_map[t_c] = {}
            
            if doc_label not in doc_topics_map[t_c]:
                doc_topics_map[t_c][doc_label] = 0
            doc_topics_map[t_c][doc_label] += 1

        d_index += 1
    f.close()

def prune_doc_topics_map():
    for k,v in doc_topics_map.iteritems():
        v = sorted(v.iteritems(),key=lambda x:x[1],reverse=True)
        v = v[0:20]
        doc_topics_map[k] = {}
        for vv in v:
            doc_topics_map[k][vv[0]] = vv[1]


def calculate_label_probility_for_topics():
    for k,v in doc_topics_map.iteritems():
        topic_label_counts = map(lambda x:x[1],v.iteritems())
        n = sum(topic_label_counts)
        v = map(lambda x:(x[0],float(x[1])/float(n)), v.iteritems())
        doc_topics_map[k] = {}
        for vv in v:
            doc_topics_map[k][vv[0]] = vv[1]

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
        word_topic_map[word][t_c] = pr
    
    f.close()

def get_probability(a,b):
    r = 0
    r = - (math.log10(a) + math.log10(b))
    return r

def get_text(doc_id):
    #print doc_id
    c.execute("select * from doc_frequency where doc_id = %s ", (doc_id))
    rr = []
    for r in c:
        rr.append(r[1])
        
    #print rr
    return rr

def print_stats(word, result):
    #print word
    if word in word_topic_map:
        topics = word_topic_map[word]
        for topic,topic_pr in topics.iteritems():
            if topic in doc_topics_map:
                labels = doc_topics_map[topic]
                for label, label_pr in labels.iteritems():
                    r = get_probability(topic_pr, label_pr)
                    if label not in result:
                        result[label] = 0
                    result[label] += r
                #print ">>>", label

def test_file(fname):
    doc_id = fname
    text = get_text(doc_id)

    r = {}
    for word in text:
        print_stats(word, r)
        
    if "ebs" in r:
        print ">>>>" , r
    '''
    v = sorted(r.iteritems(),key=lambda x:x[1],reverse=True)
    print v
    rr = ""
    if len(v) > 0:
        rr = v[0][0]
    return rr
    '''

#print "loading word map .."
#load_word_map(ff)
#print word_map
#print "loading topic word map .."
#load_topic_word_map(tw)        
#print topic_word_map

#print "loading document index.."
load_doc_index(train)
#print doc_index
#print "loading topics belonging to file.."
load_doc_topics(doc_topics_file)
calculate_label_probility_for_topics()
prune_doc_topics_map()
#print "loading word topic probabilites"
load_word_topic_probabilities(topic_words)

tr = open(train)
for did in tr:
    did = did.strip()
    o = did.split("/")[1]
    test_file(did)
    print
    #print test_file(did) , o
tr.close()

db.close()
