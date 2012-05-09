
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

def generate_input_files(src_dir, test_dir):
    for l in os.listdir(src_dir):
        l = l.strip()
        if "svn" in l:
            continue
        user = l
        user_train_dir = os.path.join(src_dir, l)
        user_test_dir = os.path.join(test_dir, l)
        command = "java -cp bin/:bin/lucene-core-3.5.0.jar:bin/lucene-analyzers-3.5.0.jar:bin/lucene-snowball-3.0.1.jar mailClassifier %s.train.txt %s.test.txt %s %s" % (user,user,user_test_dir,user_train_dir)

        print command
        os.system(command)

def run_svm():
    for l in os.listdir(src_dir):
        l = l.strip()
        if "svn" in l:
            continue
        user = l
        user_train_file = "%s.train.txt" % (l)
        user_test_file = "%s.test.txt" % (l)
        command = "python easy.py %s %s" % (user_train_file, user_test_file)

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

        command = "../../libs/mallet/bin/mallet train-topics --input %s --num-topics %s --output-model %s.topic.model --output-doc-topics %s.doc.topics --output-topic-keys %s.topic.words --inferencer-filename %s.topic.inferencer --num-iterations 500 --num-top-words 5 --num-threads 4" % (l, get_topic_count(src_dir, user), user, user, user, user) 

        print command
        os.system(command)

def infer_topics_for(src_dir):
    to_check = ".".join([src_dir, "mallet"])
    for l in os.listdir("."):
        l = l.strip()
        user = get_user(l)
        if l.endswith(to_check) == False:
            continue

        command = "../../libs/mallet/bin/mallet infer-topics --input %s.%s --inferencer %s.topic.inferencer --output-doc-topics %s.test.doc.topics --num-iterations 500 " % (user, to_check, user, user)

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

def build_svm_files():
    os.system("make clean")
    os.system("make")


generate_input_files(src_dir, test_dir)
build_svm_files()
run_svm()
