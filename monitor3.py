import commands
import datetime
import re

def newyaxis(command):
        date6=(datetime.datetime.now()-datetime.timedelta(days=6)-datetime.timedelta(hours=5)).strftime("%Y%m%d")
        value=[]
        querylist=connection.cursor()
        querylist.execute('select value from server_monitor where date>='+date6+' and command="'+command+'"')
        query=querylist.fetchall()
        for item in query:
                value.append(int(item[0]))

        maxval=max(value)
        minval=min(value)
        if command=="wc":
                minval=0
        if (maxval-minval)%8 != 0:
                maxval=maxval+(8-(maxval-minval)%8)

        yaxisvals=[]
        yaxisvals.append(str(maxval))
        yaxisvals.append(str(minval))
        yaxisvals.append(str((maxval+minval)/8.0))

        return yaxisvals


def xaxis(date,command):
        hours=width=xaxislist=converttime=converttimehr=minutes=hm=grid=hm4=hm8=hm12=hm16=hm20=""
        dst=commands.getoutput("date")
        if re.search("E.T",dst):
                dst=re.sub("^.*E","E",dst)
                dst=re.sub("T.*","T",dst)
                if dst=="EDT":
                        converttime=(datetime.datetime.utcnow()-datetime.timedelta(hours=4)).strftime("%Y%m%d")
                        converttimehr=int((datetime.datetime.utcnow()-datetime.timedelta(hours=4)).strftime("%H"))
                if dst=="EST":
                        converttime=(datetime.datetime.utcnow()-datetime.timedelta(hours=5)).strftime("%Y%m%d")
                        converttimehr=int((datetime.datetime.utcnow()-datetime.timedelta(hours=5)).strftime("%H"))
        if re.search("America",dst):
                converttime=(datetime.datetime.utcnow()-datetime.timedelta(hours=5)).strftime("%Y%m%d")
                converttimehr=int((datetime.datetime.utcnow()-datetime.timedelta(hours=5)).strftime("%H"))
        if date==converttime:
                hours=converttimehr
                minutes=int(datetime.datetime.utcnow().strftime("%M"))
                width=int(((60*hours)+minutes)/7)
                hm=hours+(minutes/60.0)
                hm4="%0.3f" % (4/hm)
                hm8="%0.3f" % (8/hm)
                hm12="%0.3f" % (12/hm)
                hm16="%0.3f" % (16/hm)
        hm20="%0.3f" % (20/hm)
        
        if hours<4 and command!="load":
            width=width
        if hours<4 and command=="load":
            width=width
        if hours>=4 and hours<8:
            width=width
            grid="&chm=R,808080,0,"+str(float(hm4)-.001)+","+str(float(hm4)+.002)
        if hours>=8 and hours<12:
            grid="&chm=R,808080,0,"+str(float(hm4)-.001)+","+str(float(hm4)+.002)+"|R,808080,0,"+str(float(hm8)-.001)+","+str(float(hm8)+.002)
        if hours>=12 and hours<16:
            grid="&chm=R,808080,0,"+str(float(hm4)-.001)+","+str(float(hm4)+.002)+"|R,808080,0,"+str(float(hm8)-.001)+","+str(float(hm8)+.002)+"|R,808080,0,"+str(float(hm12)-.001)+","+str(float(hm12)+.002)
        if hours>=16 and hours<20:
            grid="&chm=R,808080,0,"+str(float(hm4)-.001)+","+str(float(hm4)+.002)+"|R,808080,0,"+str(float(hm8)-.001)+","+str(float(hm8)+.002)+"|R,808080,0,"+str(float(hm12)-.001)+","+str(float(hm12)+.002)+"|R,808080,0,"+str(float(hm16)-.001)+","+str(float(hm16)+.002)
        if hours>=20:
            grid="&chm=R,808080,0,"+str(float(hm4)-.001)+","+str(float(hm4)+.002)+"|R,808080,0,"+str(float(hm8)-.001)+","+str(float(hm8)+.002)+"|R,808080,0,"+str(float(hm12)-.001)+","+str(float(hm12)+.002)+"|R,808080,0,"+str(float(hm16)-.001)+","+str(float(hm16)+.002)+"|R,808080,0,"+str(float(hm20)-.001)+","+str(float(hm20)+.002)
        
    else:
        hours=0
        width=205
        grid="&chm=R,808080,0,.166,.169|R,808080,0,.333,.335|R,808080,0,.499,.502|R,808080,0,.666,.668|R,808080,0,.832,.834"
        
    return hours,width,grid
        
        
def chart(command,daterange):
    tempdata=""
    for dateitem in daterange:
        i=0
        numberstring=""
        numbers=[]
        querylist=connection.cursor()
        querylist.execute('select value from server_monitor where date='+dateitem[1]+' and command="'+command+'" order by time')
        query=querylist.fetchall()
        for item in query:
            i+=1
            numbers.append(float(item[0]))
            if i!=1:
                numberstring=numberstring+","+str(item[0])
            else:   
                numberstring+=str(item[0])
        
        if not numbers:
            numbers=[0]
        
        hours,width,grid=xaxis(dateitem[1],command)
        if command=="memory":
            tempdata+='<div id="memory">\n<img src="http://chart.apis.google.com/chart?cht=lc&chs=28x232&chf=bg,s,00000080&chco=0088ff&chd=t:0,0,0&chxt=y&chxs=0,808080&chxr=0,300,1052,94&chds=300,1052"></div>'
            yaxisvals=["1052","300","69"]
        else:
            yaxisvals=newyaxis(command)
            if command=="load":
                tempdata+='<div id="'+command+'">\n<img src="http://chart.apis.google.com/chart?cht=lc&chs=22x235&chf=bg,s,00000080&chco=0088ff&chd=t:0,0,0&chxt=y&chxs=0,808080&chxr=0,'+yaxisvals[1]+','+yaxisvals[0]+','+yaxisvals[2]+'&chds='+yaxisvals[1]+','+yaxisvals[0]+'"></div>'
            else:
                tempdata+='<div id="'+command+'">\n<img src="http://chart.apis.google.com/chart?cht=lc&chs=28x235&chf=bg,s,00000080&chco=0088ff&chd=t:0,0,0&chxt=y&chxs=0,808080&chxr=0,'+yaxisvals[1]+','+yaxisvals[0]+','+yaxisvals[2]+'&chds='+yaxisvals[1]+','+yaxisvals[0]+'"></div>'
                tempdata+='<div id="'+dateitem[0]+''+command+'">\n<img src="http://chart.apis.google.com/chart?cht=lc&chf=bg,s,00000080&chco=0088ff&chs='+str(width)+'x225&chd=t:'
                tempdata+=numberstring
                tempdata+="&chds="+yaxisvals[1]+","+yaxisvals[0]+grid+"&chg=0,25"
                tempdata+='"></div>\n'

        return tempdata

def chartheaders(commandlist,daterange):
    tempdata=""
    return tempdata

def dates():
    datesquery=connection.cursor()
    datesquery.execute('select distinct date from server_monitor order by date desc limit 7')
    dates=datesquery.fetchall()
    daterange=[]
    for x in range(7):
        temp=[]
        temp.append("day"+str(x))
        temp.append(str(dates[x][0]))
        daterange.append(temp)
    daterange.reverse()
    return daterange


if '__name__'=='__main__':
    daterange=dates()
    data=""
    commandlist=['load','memory','wc']
    data+=chartheaders(commandlist,daterange)

    for command in commandlist:
            data+=chart(command,daterange)

    print data

