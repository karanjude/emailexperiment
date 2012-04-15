import MySQLdb
import math
import sys

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()

o = open(sys.argv[1],"w")
train = open("train.txt")

cached_wid_given_cj = {}
n_c_i = {}
nc = {}
vocab = {}
cj_di = {}
doc_count = 0

def build_word_count_from_document(doc_id):
    c.execute("select *  from doc_frequency where doc_id = %s",(doc_id))
    
    d = {}

    for r in c:
        word_id = r[1]
        count = int(r[2])

        if word_id not in d:
            d[word_id] = 0

        d[word_id] = count
            
    return d

def populate_word_count_from_file(doc_id, class_id):
    c.execute("select *  from doc_frequency where doc_id = %s",(doc_id))
    for r in c:
        word_id = r[1]
        count = int(r[2])
        
        if word_id not in n_c_i[class_id]:
            n_c_i[class_id][word_id] = 0
            
        n_c_i[class_id][word_id] += count
        nc[class_id] += 1

        if word_id not in vocab:
            vocab[word_id] = 0

        vocab[word_id] += 1

def train_from_file(path, class_id):
    if class_id not in n_c_i:
        n_c_i[class_id] = {}

    if class_id not in nc:
        nc[class_id] = 0

    if class_id not in cj_di:
        cj_di[class_id] = 0

    cj_di[class_id] += 1

    populate_word_count_from_file(path, class_id)
    global doc_count

    doc_count += 1

print "Building model ..."
for l in train:
    l = l.strip()
    p = l.split("/")
    user_id = p[0]
    label = p[1]
    file_name = p[2]
    path = l
    train_from_file(path, label)

train.close()
print "Model Built...."
print "Testing Model..."

test = open("test.txt")

def calculate_cj(label):
    n = cj_di[label]
    global doc_count
    d = doc_count
    r = math.log10(n) - math.log10(d)
    return r

def preprocess_wid_given_cj():
    cc = len(vocab.keys())
    
    for c_id in n_c_i:
        cached_wid_given_cj[c_id] = {}
        
        for w_id in vocab:
            if w_id not in n_c_i[c_id]:
                cached_wid_given_cj[c_id][w_id] = 1
                continue

            n = n_c_i[c_id][w_id] + 1
            denom = nc[c_id] + cc
            r = (math.log10(n) - math.log10(denom))
            
            cached_wid_given_cj[c_id][w_id] = r


def calculate_di_given_cj(d, label):
    r = 0

    for w_id in d:
        v1 = d[w_id]

        v2 = 1
        if w_id in cached_wid_given_cj[label]:
            v2 = cached_wid_given_cj[label][w_id]

        r += v1 * v2
           
    return r

def test_for_file(doc_id, label):
    d = build_word_count_from_document(doc_id)
    
    predicted_label = ""
    pr = None

    result = [label]
    

    for c_id in n_c_i:
        v1 = calculate_cj(c_id)
        v2 = calculate_di_given_cj(d, c_id)
        r = -(v1 + v2)
        
        if pr is None:
            pr = r
            predicted_label = c_id
        elif r > pr:
            pr = r
            predicted_label = c_id
        
    result.append(pr)
    result.append(predicted_label)

    result = map(str, result)

    oo =  " ".join(result)
    print oo
    o.write(oo)
    o.write("\n")

print "Preprocessing "
preprocess_wid_given_cj()

for l in test:
    l = l.strip()
    p = l.split("/")
    user_id = p[0]
    label = p[1]
    file_name = p[2]
    path = l
    test_for_file(path, label)

test.close()

db.close()
o.close()
