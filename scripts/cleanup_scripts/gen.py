import sys
import os


train = open(sys.argv[1])
input = sys.argv[3]
output = sys.argv[4]


for l in train:
    l = l.strip()
    p = l.split("/")
    user_name = p[0]
    label_name = p[1]
    file_name = p[2]
    file_to_copy = os.path.join(input, l)
    dest_path = "%s/%s/%s" % (output, user_name, label_name)
    print "making dir ", dest_path 
    command = "mkdir -p %s" % (dest_path)
    os.system(command)
    print "copying ", file_to_copy , " to ", dest_path
    command = "cp %s %s" % (file_to_copy,dest_path )
    os.system(command)


train.close()

