import MySQLdb
import math
import sys

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()

vocab = {}
docs = {}
doc_length_prob = {}
doc_length = {}
doc_word_count = {}
class_prob = {}
classes = {}
doc_probs = {}
doc_prob_given_class = {}
word_class_probs = {}

o = open(sys.argv[1],"w")

def get_doc_length(doc_id):
    if doc_id in doc_length:
        return doc_length[doc_id]

    c.execute("select * from doc_length where doc_id = %s", (doc_id))
    d = c.fetchone()[1]
    doc_length[doc_id] = d
    return d

def get_doc_length_prob(doc_id):
    if doc_id in doc_length_prob:
        return doc_length_prob[doc_id]

    c.execute("select length,count(*)/20562 as pr from doc_length group by length having length = (select length from doc_length where doc_id=%s)",(doc_id));
    prob = c.fetchone()[1]
    doc_length_prob[doc_id] = prob
    return prob

def get_doc_word_count(doc_id, word):
    if (doc_id,word) in doc_word_count:
        return doc_word_count[(doc_id,word)]

    c.execute("select *  from doc_frequency where doc_id = %s and word = %s",(doc_id, word))
    r = c.fetchone()
    rr = 0
    if r is not None:
        rr = int(r[2])
    doc_word_count[(doc_id,word)] = rr
    return rr

def build_vocab(doc_id):
    c.execute("select * from doc_frequency where doc_id = %s", doc_id)
    for r in c:
        if r[1] not in vocab:
            vocab[r[1]] = 0
        vocab[r[1]] = r[2]

def get_prob_of_class_given_doc(class_id, doc_id):
    if class_id in docs[doc_id]:
        return 1
    return 0

def get_docs(doc_id):
    #c.execute("select distinct(doc_id) from doc_frequency")
    #for r in c:
    #    if r[0] not in docs:
    #doc_id = r[0]
    p = doc_id.split('/')
    user_id = p[0]
    class_id = p[1]
    doc = p[2]
    docs[doc_id] = [class_id]

def get_class_prob(class_id):
    if class_id in class_prob:
        return class_prob[class_id]

    c.execute("select * from p_label_given_d where word = %s",(class_id))
    r = c.fetchone()
    rr = float(r[1])/float(len(docs.keys()))
    class_prob[class_id] = rr
    return rr

def get_word_prob_given_class(word_id, class_id):
    num = 1
    dendom = len(vocab.keys())
    for doc_id in docs.keys():
        n_it = get_doc_word_count(doc_id, word_id)
        p_cj_given_di = get_prob_of_class_given_doc(class_id,doc_id)
        num += n_it * p_cj_given_di
    for doc_id in docs.keys():
        n_is = vocab[word_id]
        p_cj_given_di = get_prob_of_class_given_doc(class_id,doc_id)
        dendom += n_is * p_cj_given_di
    r = float(num)/float(dendom)
    
    word_class_probs[(word_id, class_id)] = r
    return r

def fact(n):
    r = 1
    if n == 0 or n == 1:
        return r
    for i in range(n,1,-1):
        r *= i
    return r

def get_prob_doc_given_class(doc_id,class_id):
    if (doc_id,class_id) in doc_prob_given_class:
        return doc_prob_given_class[(doc_id,class_id)]

    r = fact(int(get_doc_length_prob(doc_id) * get_doc_length(doc_id)))
    rr = 1
    for word_id in vocab:
        n = get_word_prob_given_class(word_id, class_id)
        n_it = get_doc_word_count(doc_id, word_id)
        rr *=float( math.pow(float(n),n_it)) / float(fact(n_it))
    r *= rr
    doc_prob_given_class[(doc_id, class_id)] = r
    return r

def get_doc_prob(doc_id):
    if doc_id in doc_probs:
        return doc_probs[doc_id]

    r = 0
    for class_id in classes:
        r += get_class_prob(class_id) * get_prob_doc_given_class(doc_id,class_id)
    doc_probs[doc_id] = r
    return r

def get_class_prob_given_doc(doc_id):
    class_id = None
    if doc_id not in docs:
        get_docs(doc_id)
        build_vocab(doc_id)
        class_id = get_classes(doc_id)

    n = get_class_prob(class_id) * get_prob_doc_given_class(doc_id, class_id)
    d = get_doc_prob(doc_id)
    r = 0
    if d > 0:
        r = float(n)/float(d)
    return r

def get_classes(doc_id):
    p = doc_id.split('/')
    user_id = p[0]
    class_id = p[1]
    doc = p[2]
    if class_id not in classes:
        classes[class_id] = 0
    classes[class_id] += 1
    return class_id
               
#get_docs()
#get_classes()
#print get_doc_length('beck-s/2001_plan/1.')
#print get_doc_length_prob('beck-s/2001_plan/1.')
#print get_doc_word_count('beck-s/2001_plan/1.','the')
#print get_prob_of_class_given_doc('2001_plan','beck-s/2001_plan/1.')
#print get_class_prob('bastos')
#print get_word_prob_given_class('the','2001_plan')
#print get_word_prob_given_class('the','bastos')
#print get_prob_doc_given_class('beck-s/2001_plan/1.','2001_plan')
#print get_doc_prob('beck-s/2001_plan/1.')

cc = db.cursor()
cc.execute("select * from timelines order by timelinevalue")
for rr in cc:
    path = rr[2] + "/" + rr[1]
    r = get_class_prob_given_doc(path)
    o.write(path + " " + str(r))
    o.write("\n")
    o.flush()

db.close()
o.close()
