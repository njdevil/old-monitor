import datetime
import commands
import MySQLdb
import MySQLdb.cursors
import os
import re

if '__name__'=='__main__':
    count=[]

    date=(datetime.datetime.now()).strftime("%Y%m%d")
    time=(datetime.datetime.now()).strftime("%H%M")

    for a,b,c in os.walk('/var/log/apache2'):
        for file in c:
            data=""
            if re.search("access\.log$",file):
                data=commands.getoutput("wc -l "+os.path.join(a,file))
                data=re.sub(" .*$","",data)
                count.append(int(data))


    dbconn = MySQLdb.connect(db='monitor', host='localhost', user='......', passwd='.....', cursorclass=MySQLdb.cursors.DictCursor)

    insert=dbconn.cursor()
    insert.execute('insert into top(command,date,time,value) values("wc","'+date+'","'+time+'","'+str(sum(count))+'")')
