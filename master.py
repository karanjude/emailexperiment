import sys
import os

source = os.path.abspath(".")

print source

def run_svm():
    print 
    print "svm"
    os.chdir("svm")
    os.system("python process_data.py ../train ../test svm")
    os.chdir(source)

def run_naive_bayes_with_cc_bcc_as_features(run_command):
    print
    print "run_naive_bayes_with_cc_bcc_as_features"
    os.chdir("naive_bayes/from_cc_bcc_subject_as_features")
    if run_command:
        os.system("python gen_data_set.py ../../data/seed_train.txt ../../train train")
        os.system("python gen_data_set.py ../../data/seed_test.txt ../../test test")
        os.system("python process_data.py train test NaiveBayes")
    else:
        os.system("python process_data.py train test NaiveBayes format")
    os.chdir(source)

def run_max_ent_with_cc_bcc_as_features(run_command):
    print
    print "run_max_ent_with_cc_bcc_as_features"
    os.chdir("naive_bayes/from_cc_bcc_subject_as_features")
    if run_command:
        os.system("python process_data.py train test MaxEnt")
    else:
        os.system("python process_data.py train test MaxEnt format")
    os.chdir(source)

def run_lda_with_naive_bayes_full_email_as_features(run_command):
    print
    print "run_lda_with_naive_bayes_full_email_as_features"
    os.chdir("naive_bayes/lda")
    if run_command:
        os.system("python gen_data_set.py ../../data/seed_train.txt ../../train train")
        os.system("python gen_data_set.py ../../data/seed_test.txt ../../test test")
        os.system("python process_data.py train test NaiveBayes")
    else:
        os.system("python process_data.py train test NaiveBayes format")
    os.chdir(source)

def run_pam_with_naive_bayes_full_email_as_features(run_command):
    print
    print "run_pam_with_naive_bayes_full_email_as_features"
    os.chdir("naive_bayes/pam")
    if run_command:
        os.system("python gen_data_set.py ../../data/seed_train.txt ../../train train")
        os.system("python gen_data_set.py ../../data/seed_test.txt ../../test test")
        os.system("python process_data.py train test NaiveBayes")
    else:
        os.system("python process_data.py train test NaiveBayes format")
    os.chdir(source)

def run_naive_bayes_with_subject_as_features(run_command):
    print
    print "run_naive_bayes_with_subject_as_features"
    os.chdir("naive_bayes/from_subject_as_features")
    if run_command:
        os.system("python gen_data_set.py ../../data/seed_train.txt ../../train train")
        os.system("python gen_data_set.py ../../data/seed_test.txt ../../test test")
        os.system("python process_data.py train test NaiveBayes")
    else:
        os.system("python process_data.py train test NaiveBayes format")
    os.chdir(source)

def run_max_ent_with_subject_as_features(run_command):
    print
    print "run_max_ent_with_subject_as_features"
    os.chdir("naive_bayes/from_subject_as_features")
    if run_command:
        os.system("python process_data.py train test MaxEnt")
    else:
        os.system("python process_data.py train test MaxEnt format")
    os.chdir(source)

def run_ngram_with_naive_bayes_full_email_as_features(run_command):
    print
    print "run_ngram_with_naive_bayes_full_email_as_features"
    os.chdir("naive_bayes/ngrams")
    if run_command:
        os.system("python gen_data_set.py ../../data/seed_train.txt ../../train train")
        os.system("python gen_data_set.py ../../data/seed_test.txt ../../test test")
        os.system("python process_data.py train test NaiveBayes")
    else:
        os.system("python process_data.py train test NaiveBayes format")
    os.chdir(source)

def run_naive_bayes_with_header_and_body_as_features(run_command):
    print
    print "run_naive_bayes_with_header_and_body_as_features"
    os.chdir("naive_bayes/header_body_features")
    if run_command:
        os.system("python gen_data_set.py ../../data/seed_train.txt ../../train train")
        os.system("python gen_data_set.py ../../data/seed_test.txt ../../test test")
        os.system("python process_data.py train test NaiveBayes")
    else:
        os.system("python process_data.py train test NaiveBayes format")
    os.chdir(source)

def run_max_ent_with_header_and_body_as_features(run_command):
    print
    print "run_max_ent_with_header_and_body_as_features"
    os.chdir("naive_bayes/header_body_features")
    if run_command:
        os.system("python process_data.py train test MaxEnt")
    else:
        os.system("python process_data.py train test MaxEnt format")
    os.chdir(source)

def run_naive_bayes_with_from_as_features(run_command):
    print
    print "run_naive_bayes_with_from_as_features"
    os.chdir("naive_bayes/only_from_as_features")
    if run_command:
        os.system("python gen_data_set.py ../../data/seed_train.txt ../../train train")
        os.system("python gen_data_set.py ../../data/seed_test.txt ../../test test")
        os.system("python process_data.py train test NaiveBayes")
    else:
        os.system("python process_data.py train test NaiveBayes format")
    os.chdir(source)

def run_max_ent_with_from_as_features(run_command):
    print
    print "run_max_ent_with_from_as_features"
    os.chdir("naive_bayes/only_from_as_features")
    if run_command:
        os.system("python process_data.py train test MaxEnt")
    else:
        os.system("python process_data.py train test MaxEnt format")
    os.chdir(source)

####3


os.system("curl http://people.cs.umass.edu/~ronb/datasets/enron_flat.tar.gz -o enron_flat.tar.gz") 
os.system("gunzip enron_flat.tar.gz")
os.system("mkdir -p email_small")
os.system("mv enron_flat.tar email_small")
os.chdir("email_small")
os.system("tar -xvf enron_flat.tar")

os.chdir(source)



os.system("python gen_train_test_data.py data/seed_train.txt email_small train")
os.system("python gen_train_test_data.py data/seed_test.txt email_small test")

os.system("rm email_small/enron_flat.tar")
os.system("python normalize_data.py email_small train test")



run_naive_bayes_with_cc_bcc_as_features(True)
run_max_ent_with_cc_bcc_as_features(True)

run_lda_with_naive_bayes_full_email_as_features(True)

run_pam_with_naive_bayes_full_email_as_features(True)

run_naive_bayes_with_subject_as_features(True)
run_max_ent_with_subject_as_features(True)


run_ngram_with_naive_bayes_full_email_as_features(True)

run_naive_bayes_with_header_and_body_as_features(True)
run_max_ent_with_header_and_body_as_features(True)

run_naive_bayes_with_from_as_features(True)
run_max_ent_with_from_as_features(True)

run_naive_bayes_with_cc_bcc_as_features(False)
run_max_ent_with_cc_bcc_as_features(False)

run_lda_with_naive_bayes_full_email_as_features(False)

run_pam_with_naive_bayes_full_email_as_features(False)

run_naive_bayes_with_subject_as_features(False)
run_max_ent_with_subject_as_features(False)


run_ngram_with_naive_bayes_full_email_as_features(False)

run_naive_bayes_with_header_and_body_as_features(False)
run_max_ent_with_header_and_body_as_features(False)

run_naive_bayes_with_from_as_features(False)
run_max_ent_with_from_as_features(False)

run_svm()
