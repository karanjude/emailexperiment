import sys
import os

ref_file = open(sys.argv[1])
src_dir = os.path.abspath(sys.argv[2])
dest_dir = sys.argv[3]

command = "mkdir -p " + dest_dir
os.system(command)


for file_path in ref_file:
    file_path = file_path.strip()
    parts = file_path.split("/")
    user_name = parts[0]
    label = parts[1]
    file_name = parts[2]
    
    command = "mkdir -p " + os.path.join(dest_dir,user_name)
    print command
    os.system(command)
    command = "mkdir -p " + os.path.join(dest_dir,user_name,label)
    print command
    os.system(command)
    command = "cp " + os.path.join(src_dir,file_path) + " " + os.path.join(dest_dir,user_name,label)
    print command
    os.system(command)

ref_file.close()
