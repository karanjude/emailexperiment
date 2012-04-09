import MySQLdb

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()

p_label_given_d = {}

c.execute("select doc_id from doc_frequency group by doc_id")
for r in c:
    label = r[0]
    p = label.split("/")
    if len(p) > 3:
        print label
    else:
        label = p[1]
        if label not in p_label_given_d:
            p_label_given_d[label] = 0
        p_label_given_d[label] += 1


c = db.cursor()
for k,v in p_label_given_d.iteritems():
    c.execute("insert into p_label_given_d(word,count_in_docs) values(%s,%s)", (k,v)) 
print p_label_given_d;
db.close()
