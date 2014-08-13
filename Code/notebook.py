# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:34:15 2013

@author: Alex
"""
import pandas as pd
import datetime as dt

def my_parser(x,y):
    y = str(int(y))
    hour=y[:-2]
    minute=y[-2:]
    time=dt.time(int(hour),int(minute))
    parsed=dt.datetime.combine(x,time)
    #print parsed
    return parsed

def FieldNotes(sheet,headerrow,Book):
    notebook_file = pd.ExcelFile(Book)

    notebook = notebook_file.parse(sheet,header=headerrow,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    return notebook
    
def OrangePeel(sheet,headerrow,Book):
    opfile = pd.ExcelFile(Book)
    orangepeel = opfile.parse(sheet,header=headerrow,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    orangepeel = orangepeel.drop(orangepeel.columns[16:],1)
    orangepeel = orangepeel[orangepeel['AVG L/sec']>=0]
    return orangepeel
    
#orangepeel = OrangePeel('OrangePeel',1,datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/Discharge/Fagaalu-StageDischarge.xlsx')
