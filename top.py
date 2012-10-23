import datetime
import commands
import MySQLdb
import MySQLdb.cursors
import os
import re

if '__name__'=='__main__':
    topdata=""
    topdatasplit=[]
    load=""
    memory=""
    count=[]

    date=(datetime.datetime.now()).strftime("%Y%m%d")
    time=(datetime.datetime.now()).strftime("%H%M")

    topdata=commands.getoutput("top -b -n 1")
    topdatasplit=topdata.split("\n")
    load=topdatasplit[0]
    memory=topdatasplit[3]

    load=re.sub("^.*load average: ","",load)
    load=re.sub(",.*","",load)
    load=float(load)
    load=str(load*100)
    memory=re.sub("^.*total,","",memory)
    memory=re.sub("k used,.*","",memory)
    memory=re.sub("\s","",memory)
    memory=float(memory)
    memory=str(round(memory/1000,0))

    for a,b,c in os.walk('/var/log/apache2'):
        for file in c:
            data=""
                if re.search("access\.log$",file):
                    data=commands.getoutput("wc -l "+os.path.join(a,file))
                    data=re.sub(" .*$","",data)
                    count.append(int(data))

    dbconn = MySQLdb.connect(db='monitor', host='localhost', user='.....', passwd='......', cursorclass=MySQLdb.cursors.DictCursor)

    insert=dbconn.cursor()
    insert.execute('insert into intf.server_monitor(command,date,time,value) values("load","'+date+'","'+time+'","'+load+'")')
    insert.execute('insert into intf.server_monitor(command,date,time,value) values("memory","'+date+'","'+time+'","'+memory+'")')
    insert.execute('insert into intf.server_monitor(command,date,time,value) values("wc","'+date+'","'+time+'","'+str(sum(count))+'")')

