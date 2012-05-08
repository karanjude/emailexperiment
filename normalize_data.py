import sys
import os

base_dir = sys.argv[1]
train_dir = sys.argv[2]
test_dir = sys.argv[3]

def get_diff(user, train, test):
    train = os.path.join(os.path.abspath(train), user)
    test = os.path.join(os.path.abspath(test), user)
    train_labels = set([x for x in os.listdir(train)])
    test_labels = set([x for x in os.listdir(test)])
    to_delete_train = train_labels - test_labels
    to_delete_test = test_labels - train_labels
    for r in to_delete_train:
        command = "rm -r %s/%s" % (train,r)
        print command
        os.system(command)
    for r in to_delete_test:
        command = "rm -r %s/%s" % (test,r)
        print command
        os.system(command)
        

    

for l in os.listdir(base_dir):
    l = l.strip()
    if "svn" in l:
        continue
    user = l
    get_diff(user, train_dir, test_dir)
    
