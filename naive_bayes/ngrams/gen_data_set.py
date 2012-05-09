import sys
import os

ref_file = open(sys.argv[1])
src_dir = os.path.abspath(sys.argv[2])
dest_dir = sys.argv[3]

command = "mkdir -p " + dest_dir
os.system(command)

def filter_file_contents(file_name , file_path, dest_path):
    try:
        f = open(file_path)
    except IOError:
        return
    r = []

    tags = ["from:","bcc:","cc:","subject:"]
    skip_tags = ["Message-ID:","Date:","Mime-Version:","Content-Type:","Content-Transfer-Encoding:","X-","To:"]

    count = 0
    for l in f:
        l = l.strip()
        skip = False
        for s_tag in skip_tags:
            if l.startswith(s_tag):
                skip = True
                break

        if skip:
            continue
        
        l = l.lower()

        for tag in tags:
            if l.startswith(tag) and count < 15:
                l = l.replace(tag,"")
                l = l.replace(","," ")
                break
            #print l
        #print l
        r.extend(l.split())

        count += 1

    content = " ".join(r)

    f.close()

    p = dest_path.split("/")
    n = len(p)
    p = "/".join(p[:n-1])

    command = "mkdir -p " + p
    os.system(command)
    fw = open(dest_path , "w")
    fw.write(content)
    fw.close()

for file in ref_file:
    file = file.strip()
    file_path = os.path.join(src_dir, file)
    p = file.split("/")
    user_name = p[0]
    label = p[1]
    file_name = p[2]

    src_file_path = os.path.join(src_dir,file)
    dest_path = os.path.join(dest_dir,user_name,label,file_name)

    print file_name , src_file_path, dest_path
    filter_file_contents(file_name , src_file_path, dest_path)

ref_file.close()
