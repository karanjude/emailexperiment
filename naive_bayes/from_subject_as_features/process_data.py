
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
        command = "../../libs/mallet/bin/mallet train-classifier --input %s.mallet --output-classifier %s_%s.classifier --trainer %s" % (l,l,trainer,trainer)
        print command
        os.system(command)

def generate_mallet_files(src_dir):
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        command = "../../libs/mallet/bin/mallet import-dir --input %s --output %s.mallet" % (user_dir , l)
        print command
        os.system(command)

def test_classifier(src_dir, trainer):
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        command = "../../libs/mallet/bin/mallet classify-dir --input %s/%s/* --output %s_%s.out --classifier %s_%s.classifier" % (test_dir,l,l,trainer,l,trainer)
        print command
        os.system(command)

def generate_accuracy(src_dir, trainer):
    for l in os.listdir(src_dir):
        l = l.strip()
        user_dir = os.path.join(src_dir, l, "*")
        command = "python accuracy.py  %s_%s.out.final %s > %s_%s.out.accuracy" % (l,trainer,1,l,trainer)
        print command
        os.system(command)
        for i in range(3,11,2):
            command = "python accuracy.py  %s_%s.out.final %s >> %s_%s.out.accuracy" % (l,trainer,i,l,trainer)
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
#build_classifierss(src_dir, trainer)
#test_classifier(src_dir, trainer)
#filter_output(src_dir,trainer)
#generate_accuracy(src_dir, trainer)
format_accuracy(src_dir, trainer)
