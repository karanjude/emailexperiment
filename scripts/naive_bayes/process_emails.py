import sys
import MySQLdb
import os
import string

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()
s = sys.argv[1]

def insert_to_db(path,parts):
    d = {}
    for p in parts:
        if p not in d:
            d[p] = 1
        else:
            d[p] += 1
    print path
    for k,v in d.iteritems():
        print k,v
        c.execute("insert into doc_frequency(doc_id,word,count) values(%s,%s,%s)", (path,k,v))
    

to_filter = [
    'Message-ID:',
    'Date:',
    'From:',
    'To:',
    'Cc:',
    'Bcc',
    'Subject:',
    'Mime-Version:',
    'Content-Type:',
    'Content-Transfer-Encoding:',
    'X-From:',
    'X-To:',
    'X-cc:' ,
    'X-bcc:',
    'X-Origin:',
    'X-FileName:']

def process_file(ff,path):
    print 
    f = open(ff)
    body_parts = []
    l = f.readline()
    is_header = True
    while len(l) > 0:
        l = l.strip().lower()
        if is_header == True and len(l) == 0:
            is_header = False

        if l.endswith("="):
            l1 = f.readline()
            l = l[:-1] + l1
        elif l.endswith("=20"):
            l = l[:-3]
        else:
            if is_header == False:
                table = "abcdefghijklmnopqrstuvwxyz "
                l = filter(lambda x:x in table,l)

                if len(l) > 0:
                    body_parts.append(l)
                
            l = f.readline()
    r = "\n".join(body_parts)
    insert_to_db(path, r.split())
    f.close()

c.execute("select * from timelines");
for r in c:
    p = os.path.join(os.path.abspath(s),r[2],r[1])
    print p
    process_file(p,os.path.join(r[2],r[1]))

db.close()
