import urllib2
import os
import datetime
from BeautifulSoup import BeautifulSoup
import csv

## Grabs wave parameter data from NDBC station
## http://www.ndbc.noaa.gov/station_page.php?station=nstp6
datagrab = True

if datagrab == True:
    slist = ['NSTP6'] ##stations needed
    ylist = ['2014'] ##years needed
    mlist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']#,'Sep','Oct','Nov','Dec'] ##months needed
    mdict = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    alldata = open('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/'+'2013.txt','w')
    for s in slist:
        for y in ylist:
            for m in mlist:
                try:
                    f = open('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/' +s+ '_' +y+ '_' +m+ '.csv', 'w') ##enter directory for download
                    url = 'http://www.ndbc.noaa.gov/view_text_file.php?filename=nstp6'+str(mdict[m])+y+'.txt.gz&dir=data/stdmet/'+m+'/' ##enter web address of data
                    print url
                    page = urllib2.urlopen(url)
                    soup = BeautifulSoup(page)
                    print s + ','+ y + ',' + m
        ##            for line in soup:
        ##                print line
                    f.write(str(soup))
                    alldata.write(str(soup))
                    print
                    f.close()
                except:
                    pass

### Append all
#files = os.listdir('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/')
#alldata = open('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/'+'2014.txt','w')
#for f in files:
#    if f.endswith('.csv')==True:
#        print f
#        with open(f,'wb') as csvfile:
#            data=csv.reader(csvfile,dialect='excel')
#            for row in data:
#                alldatata.write(row)
#        
### Analyze data
##files = os.listdir('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6')
##barolist = []
##for f in files:
##    if f.endswith('.csv') == True:
##        print f
##        data = open(f,'r')
##        for line in data:
##            d = line.strip('\n').split()
##            if d[0].isdigit()==True:
##                year,month,day = d[0],d[1],d[2]
##                hour,minute = d[3],d[4]
##                time = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute))
##                pressure = d[12]
##                #print pressure
##                barolist.append((time,pressure))
##

