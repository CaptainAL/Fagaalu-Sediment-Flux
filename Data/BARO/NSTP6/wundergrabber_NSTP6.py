# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 12:45:57 2014

@author: Alex
"""

import urllib2
import os
import datetime
from BeautifulSoup import BeautifulSoup
import csv

## Grabs wave parameter data from NDBC station
## http://www.ndbc.noaa.gov/station_page.php?station=nstp6
datagrab = True

if datagrab == True:
    s = 'NSTU' ##stations needed
    daterange = date_range('20120101 00:00:00',now,freq='D')
    
    alldata = open('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/NSTP6.csv','w')
    columns = ['TimeSST','TemperatureF','Dew PointF','Humidity','Sea Level PressureIn','VisibilityMPH','Wind Direction','Wind SpeedMPH','Gust SpeedMPH','PrecipitationIn','Events','Conditions','WindDirDegrees','DateUTC']
    datalist = [] ## write header columns in empty DataFrame
    for date in daterange:
        if date < now:
#            print date
            try:
                url = 'http://www.wunderground.com/history/airport/'+s+'/'+str(date.year)+'/'+str(date.month)+'/'+str(date.day)+'/DailyHistory.html?req_city=NA&req_state=NA&req_statename=NA&format=1'##enter web address of data
                url = 'http://www.ndbc.noaa.gov/view_text_file.php?filename=nstp6'+str(date.month)+str(date.year)+'.txt.gz&dir=data/stdmet/'+str(date.month)+'/' ##enter web address of data                
                #print url
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page)
                soupsplit = str(soup.tagStack).split('\n')
    
                for line in soupsplit[2:-1]:
                    if line != None:
                        dt = to_datetime(str(date.month)+'/'+str(date.day)+ '/'+ str(date.year)+' '+line.split(',')[0])
                        data = line.split(',')
                        datalist.append((dt,[data[0],float(data[1]),float(data[2]),float(data[3]),float(data[4]),float(data[5]),data[6],float(data[7]),data[8],data[9],data[10],data[11],data[12],data[13]])) ##append tuple to list
#                        print dt
            except:
#                print 'skipped day'
                pass
        else:
            pass
    frame = DataFrame.from_items(datalist,orient='index',columns=columns)
    frame.columns = columns
    frame = frame.applymap(lambda x: np.nan if x=='-9999' else x)
    datafile =  frame.to_csv('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTU/NSTU-current.csv')
   