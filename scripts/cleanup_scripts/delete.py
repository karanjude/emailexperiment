import sys
import MySQLdb
import os
import string

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()
cc = db.cursor()
#c.execute("select * from doc_frequency group by word having count = 1");
#c.execute("select * from word_count order by all_count desc limit 50");
#for r in c:
#    print "deleting word ", r[0];
#    cc.execute("delete from doc_frequency where word = %s", (r[0]))

ff = sys.argv[1]
f = open(ff)
for l in f:
    w = l.strip()
    print "deleting word ", w
    cc.execute("delete from doc_frequency where word = %s", (w))

f.close()
db.close()
