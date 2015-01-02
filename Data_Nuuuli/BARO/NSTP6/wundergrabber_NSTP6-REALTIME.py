# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 12:45:57 2014

This is to get the REALTIME (Last 45 days) and use it

@author: Alex
"""

import urllib2
import os
import datetime
from BeautifulSoup import BeautifulSoup
from pandas import DataFrame, to_datetime, date_range
import numpy as np

## Grabs wave parameter data from NDBC station
## http://www.ndbc.noaa.gov/data/realtime2/NSTP6.txt


datagrab = True


if datagrab == True:
    print 'Grabbing NSTP6 REALTIME data...'
    
    columns = ['YY','MM','DD','hh','mm','WDIR','WSPD','GST','WVHT','DPD','APD','MWD','PRES','ATMP','WTMP','DEWP','VIS','PTDY','TIDE']
    datalist = [] ## write header columns in empty DataFrame

    try:
        url = 'http://www.ndbc.noaa.gov/data/realtime2/NSTP6.txt' ##enter web address of data                
        print url
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        soupsplit = str(soup.tagStack).split('\n')
    
        for line in soupsplit[2:-1]:
            if line != None:
                data = line.split()
                data_filtered = [x if x!='MM' else 999.0 for x in data]## replace No Data values (='MM' for some reason)
                date_time = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]))
        
                datalist.append((date_time,data_filtered)) ##append tuple to list
                print 'Appended data for '+str(date_time)
        
        frame = DataFrame.from_items(datalist,orient='index',columns=columns)
        frame = frame.convert_objects(convert_numeric=True)
        frame = frame.sort()
    
        datafile =  frame.to_csv(path_or_buf='C:/Users/Alex/Documents/GitHub/Fagaalu-Sediment-Flux/Data/BARO/NSTP6/NSTP6-RealTime_12_30_14.csv',
                                 sep=' ',index=False)
        
    except:
        raise

        pass


else:
    pass
    
   