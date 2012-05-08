
import sys
import os

src_dir = sys.argv[1]
test_dir = sys.argv[2]
if len(sys.argv) > 3:
    trainer = sys.argv[3]
else:
    trainer = ""


def build_classifierss(src_dir, trainer):
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        command = "../../libs/mallet/bin/mallet train-classifier --input %s.mallet --output-classifier %s_%s.classifier --trainer %s " % (l,l,trainer,trainer)
        print command
        os.system(command)

def generate_mallet_files(src_dir):
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        command = "../../libs/mallet/bin/mallet import-dir --input %s --output %s.%s.mallet --keep-sequence --remove-stopwords --keep-sequence-bigrams" % (user_dir , l, src_dir)
        print command
        os.system(command)

def get_user(l):
    p = l.split(".")
    return p[0]

def get_topic_count(src, user):
    dir_to_check = os.path.abspath(os.path.join(src, user))
    c = 0
    for l in os.listdir(dir_to_check):
        l = os.path.join(dir_to_check, l)
        if os.path.isdir(l):
            c += 1
    return c

def generate_topic_inferers(src_dir):
    to_check = ".".join([src_dir, "mallet"])
    for l in os.listdir("."):
        l = l.strip()
        user = get_user(l)
        if l.endswith(to_check) == False:
            continue

        command = "../../libs/mallet/bin/mallet train-topics --input %s --num-topics %s  --output-doc-topics %s.doc.topics  --num-iterations 100 --num-top-words 5 --num-threads 4 --use-pam true" % (l, get_topic_count(src_dir, user), user) 

        print command
        os.system(command)

def infer_topics_for(src_dir):
    to_check = ".".join([src_dir, "mallet"])
    for l in os.listdir("."):
        l = l.strip()
        user = get_user(l)
        if l.endswith(to_check) == False:
            continue

        command = "../../libs/mallet/bin/mallet train-topics --input %s --num-topics %s --output-doc-topics %s.test.doc.topics  --num-iterations 100 --num-top-words 5 --num-threads 4 --use-pam true" % (l, get_topic_count(src_dir, user), user) 

        print command
        os.system(command)

def gen_pmaps(src_dir):
    to_check = ".".join([src_dir, "mallet"])
    for l in os.listdir("."):
        l = l.strip()
        user = get_user(l)
        if l.endswith(to_check) == False:
            continue
    
        doc_topics_file = user + ".doc.topics"
        command = "python gen_pmap.py " + doc_topics_file
        print command
        os.system(command)

def test_classifier(src_dir):
    for l in os.listdir(src_dir):
        l = l.strip()
        command = "python gen_test_classes.py %s.test.doc.topics %s.pmap > %s.out.final" % (l,l,l)

        print command
        os.system(command)

def generate_accuracy(src_dir, trainer):
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        command = "python accuracy.py  %s.out.final %s > %s_%s.out.accuracy" % (l,1,l,trainer)
        print command
        os.system(command)
        for i in range(3,11,2):
            command = "python accuracy.py  %s.out.final %s >> %s_%s.out.accuracy" % (l,i,l,trainer)
            print command
            os.system(command)

def format_accuracy(src_dir, trainer):
    rr = [0] * 5
    n = 0
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        f = open("%s_%s.out.accuracy" % (l,trainer))
        r = []
        for ll in f:
            ll = ll.strip()
            r.append(ll)
        f.close()
        print l , " ".join(r) 
        for i in range(0,len(r)):
            rr[i] += float(r[i])
        n += 1

    rr = map(lambda x:float(x)/float(n), rr)
    print map(str,rr)
        
            

def filter_output(src_dir, trainer):
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        command = "python filter.py  %s_%s.out > %s_%s.out.final" % (l,trainer,l,trainer)
        print command
        os.system(command)


#generate_mallet_files(src_dir)
#generate_mallet_files(test_dir)
#generate_topic_inferers(src_dir)
#infer_topics_for(test_dir)
#gen_pmaps(src_dir)
#test_classifier(src_dir)
#filter_output(src_dir,trainer)
#generate_accuracy(src_dir, trainer)
format_accuracy(src_dir, trainer)
