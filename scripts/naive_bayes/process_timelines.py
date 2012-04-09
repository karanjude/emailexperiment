import MySQLdb
import os
import sys
import datetime

db = MySQLdb.connect(user="root",passwd="",db="email")
c = db.cursor()

def insert_into_db(t,u,p):
    print t,u,p
    c.execute("insert into timelines(timelinevalue,folder_path,user) values(%s,%s,%s)", (t,p,u,))

def process_file(file_name):
    f = open(file_name)
    user = os.path.basename(file_name) 
    user = user.split('.')[0]
    for l in f:
        l = l.strip()
        p = l.split()
        timeline = p[0]
        path = p[1]
        yyyy = timeline[0:4]
        mm = timeline[4:6]
        dd = timeline[6:8]
        hh = timeline[8:10]
        mmm = timeline[10:12]
        ss = "00"
        timeline = datetime.datetime(int(yyyy),int(mm),int(dd),int(hh),int(mmm),int(ss))
        insert_into_db(timeline, user, path)

s = sys.argv[1]
for f in os.listdir(s):
    process_file(os.path.join(os.path.abspath(s),f))

db.close()




