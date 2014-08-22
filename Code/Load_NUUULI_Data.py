# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 07:40:01 2014

@author: Alex
"""

#### Import modules
## Data Processing
import numpy as np
import pandas as pd
import math
import datetime as dt
import os
## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.max_rows', 15)

#### DIRECTORIES
git=True
if git==True: ## Git repository
    maindir = 'C:/Users/Alex/Documents/GitHub/Fagaalu-Sediment-Flux/' 
    datadir=maindir+'Data/'
    dataoutputdir = datadir+'Output/'
    GISdir = maindir+'Data/GIS/'
    figdir = maindir+'Figures/'
    dirs={'main':maindir,'data':datadir,'GIS':GISdir,'fig':figdir}
elif git!=True: ## Local folders
    maindir = 'C:/Users/Alex/Desktop/'### samoa/
    csvoutputdir = datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/csv_output/'
    savedir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/'
    figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    

#### LOAD MASTER_XL Data
print 'opening MASTER_DATA excel file...'+dt.datetime.now().strftime('%H:%M:%S')
if 'XL' not in locals():
    print 'Opening XL...'
    XL = pd.ExcelFile(datadir+'MASTER_DATA_NUUULI.xlsx')
if 'XL_Fagaalu' not in locals():
    print 'Opening XL_Fagaalu...'
    XL_Fagaalu = pd.ExcelFile(datadir+'MASTER_DATA_FAGAALU.xlsx')
print 'MASTER_DATA opened: '+dt.datetime.now().strftime('%H:%M:%S')


#### Import PRECIP Data
from precip_data import raingauge, AddTimu1, AddTimu1Hourly, AddTimu1Daily, AddTimu1Monthly
Precip = raingauge(XL,'Timu-Nuuuli1',0) ## (path,sheet,shift) no header needed
Precip.columns=['Timu-Nuuuli1']
Precip['Timu-Nuuuli1-15']=Precip['Timu-Nuuuli1'].resample('15Min',how='sum')
Precip['Timu-Nuuuli1-hourly']=Precip['Timu-Nuuuli1'].resample('60Min',how='sum')
Precip['Timu-Nuuuli1-daily']=Precip['Timu-Nuuuli1'].resample('1D',how='sum')

Timu_Nuuuli2 = raingauge(XL,'Timu-Nuuuli2',0) ## (path,sheet,shift) no header needed
Precip['Timu-Nuuuli2'] = Timu_Nuuuli2['Events']
Precip['Timu-Nuuuli2-15'] = Precip['Timu-Nuuuli2'].resample('15Min',how='sum')
Precip['Timu-Nuuuli2-hourly']=Precip['Timu-Nuuuli2'].resample('60Min',how='sum')
Precip['Timu-Nuuuli2-daily']=Precip['Timu-Nuuuli2'].resample('1D',how='sum')

#### Import WX STATION Data
from load_from_MASTER_XL import WeatherStation

FPa = WeatherStation(XL_Fagaalu,'FP-30min')
Bar15Min=FPa['Bar'].resample('15Min',fill_method='pad',limit=2) ## fill the 30min Barometric intervals to 15minute, but not Precip!
FPa = FPa.resample('15Min')
FPa['Bar']=Bar15Min
FPb = WeatherStation(XL_Fagaalu,'FP-15min')
FP = FPa.append(FPb)

#### Import BAROMETRIC Data: NDBC,TULA,TAFUNA
def Tula(datapath=datadir+'BARO/TulaStation/TulaMetData/'):
    #### Barometric Pressure from NOAA Weather Station Tula
    print 'loading TULAbaro....'
    ylist = ['2012']
    TulaPressureList = []
    #print 'month'+'\t'+'day'+'\t'+'year'+'\t'+'mm precip'
    for y in ylist:
        path = datapath+y
        files = os.listdir(path)
        for f in files: ## each f is a new DAY
            data = open(path+'/'+f,'r')
            daysplit = f.replace('.','-').split('-')
            #dayfile = open(daysplit[1]+'-'+daysplit[2]+'-'+daysplit[0]+'.csv','w')
            year, month, day = daysplit[0],daysplit[1],daysplit[2]
            #print 'year: '+year+' month '+month+' day: '+day
            dailyprecip, precipprev, precip15, pressure = 0.0,0.0,0.0,0.0
            presscount = 0
            try:
                for d in data: ## each d is a new MINUTE
                    split = d.split(',')
                    try:
                        num =float(split[1]) #will be True if split[1] is a number and the line is data
                    except:
                        num = False
                        pass
                    if num != False: ## Make sure the line is data #
                        #print split[1]+','+split[2]+','+split[3]+','+split[4]+','+split[5]+','+split[13]+','+split[18]
                        hour,minute = split[4], split[5]
                        press = split[13] #the pressure value for the Minute, need to be agg'ed to 15min.
                        precip = split[18] ## subtract the previous Minute's precip value
                        presscount+=1
                        try: ## Running total for 15 min. aggregate
                            if float(press) == False:
                                pressure = 'NaN'
                            if float(press) != 9999:
                                pressure = pressure + float(press) ## running total of pressure?
                            if float(press) == 9999:
                                pressure = pressure + 1000
                        except:
                                pressure = 'NaN'
                                pass
                                
                        try: ## Subtract previous minute's precip from current minute to get correct value
                            if float(precip) == False:
                                precip = 'NaN'
                            if precip != 9999:
                                #print str(precip)+' - '+str(precipprev)
                                precip = float(precip)-precipprev ## subtract previous minute's precip (precipprev) from current precip (precip)
                                #print precip ## this should be the correct precip value
                                precip15=precip15+float(precip) ## Running total for 15 minute aggregated rainfall
                                precipprev = split[18]
                        except:
                                precip = 'NaN'
                                pass
                        if minute == '':
                            minute = 'NaN'
                            pass
                        ## at 15 minute intervals average pressure and tally up precip
                        if float(minute) == 0 or float(minute)==15 or float(minute)==30 or float(minute)==45: ## Adjust time offset???
                                pressure15 = float(pressure)/presscount ## Get 15 minute average pressure 
                                dailyprecip = dailyprecip+float(precip) ## Aggregate daily rainfall
                                #print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15)+'\t'+str(precip15) 
                                #print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15) ## tab-separated output
                                Time = dt.datetime(int(year),int(month),int(day),int(hour),int(minute)) ## -10 so it lines up with other times
                                #print Time
                                timedelta =-dt.timedelta(hours=11)
                                Time = Time + timedelta ## time offset to get it to match Faga'alu
                                #print Time
                                TulaPressureList.append((Time,float(pressure15))) ## make list of 15 minute averaged atmospheric pressure
                                precipprev = split[18] ## reassign precip to precipprev for next loop
                                precip15,pressure,presscount = 0.0,0.0,0 ## reset variables for next loop
            except:
                    raise
            #print month+'\t'+day+'\t'+year+'\t'+str(dailyprecip)
    datadict = dict(TulaPressureList) ## Make dictionary of (Time,Pressure) tuples, RAW data
    baro = pd.Series(datadict,name='TULAbaro')
    baro_offset = (baro/10.0)+.92
    return baro_offset

## To get more NSTP6 data either go to their website and copy and paste the historical data
## or use wundergrabber_NSTP6-REALTIME.py and copy and paste frome the .csv
def ndbc(datapath=datadir+'BARO/NSTP6/'):
    print 'loading NDBC baro...'
    ## Analyze data
    path = datapath
    barolist = []
    #files = os.listdir(path) ## if multiple monthly files are needed uncomment this line and comment out the block below
    ##data = open(path+'/'+f,'r')
    ##for f in files:
    ##    if f.endswith('.csv') == True:
    ##        print f
    f='NSTP6-2012-14.txt'
    with open(path+'/'+f,'r') as lines:
        first_press = lines.readlines()[2].split()[12]
    data = open(path+'/'+f,'r')
    
    pressureprev=first_press ## get a first value to use
    #print str(pressureprev)
    misscount = 0
    for line in data:
        d = line.strip('\n').split()
        #print d
        if d[0].isdigit()==True:
            year,month,day = d[0],d[1],d[2]
            hour,minute = d[3],d[4]
            time = dt.datetime(int(year),int(month),int(day),int(hour),int(minute))
            pressure = d[12]
            if pressure != '9999.0':
                pressureprev = pressure
                misscount=0
            ## Handle missing values: If 1 or 2 are missing, keep previous value
            ## if more than 2 are missing then there is No Data
            elif pressure == '9999.0' and misscount <= 2: ##if it's just 1 or 2 missing values, just keep the previous value
                pressure = pressureprev ## fill in previous value
                misscount+=1 ## count up one for the missing value
            elif pressure == '9999.0' and misscount >2: ##if missing more than 2 values than it's 'NaN'
                pressure = 'NaN' ## fill in None value
                pressureprev = 'NaN' ## fill in None value
                misscount+=1 ## count up one for the missing value
            else:
                print 'NDBC pressure cannot be determined for '+str(time)
            #print time,pressure,pressureprev
            barolist.append((time,pressure))
              
    NDBCbarometric = []
    for line in barolist:
        #print line
        time = line[0]
        pressure = float(line[1])/10 ## convert kPa to hPa
        if time.minute == 12 or time.minute == 42:
            time = time+dt.timedelta(0,0,0,0,3) #add 3 minutes to round up

        ## Date/Time offset to match Faga'alu weather station
        ## Shift NDBC -11 hours (UTC to local time)
        timedelta =-dt.timedelta(hours=11) ### UTC to local time
        time = time + timedelta ## time offset to get it to match Faga'alu
        if time.minute == 0 or time.minute == 15 or time.minute == 30 or time.minute == 45:
           #print time,pressure
            NDBCbarometric.append((time,pressure))
    datadict = dict(NDBCbarometric)
    baro = pd.Series(datadict,name='NDBCbaro')
    return baro
    
##load data from Tafuna Intl ## To get more data from the Airport run wundergrabber_NSTU.py in the 'Maindir+Data/NSTU/' folder
airport = pd.DataFrame.from_csv(datadir+'BARO/NSTU/NSTU-current.csv') ## download new data using wundergrabber
airport['Wind Speed m/s']=airport['Wind SpeedMPH'] * 0.44704
TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea Level PressureIn'] * 3.3863881579}).resample('15Min',fill_method='ffill',limit=2)## inches to kPa
TAFUNAbaro = TAFUNAbaro.reindex(pd.date_range(min(TAFUNAbaro.index),max(TAFUNAbaro.index),freq='15Min'))
##load data from NDBC NSTP6 station at DMWR, Pago Harbor
NDBCbaro = pd.DataFrame(ndbc(datadir+'BARO/NSTP6/'),columns=['NDBCbaro'])
##load data from NOAA Climate Observatory at Tula, East Tutuila
TULAbaro= pd.DataFrame(Tula(datadir+'BARO/TulaStation/TulaMetData/'),columns=['TULAbaro']) ## add TULA barometer data

## Build data frame of barometric data: Make column 'baropress' with best available data
allbaro = pd.DataFrame(TAFUNAbaro['TAFUNAbaro'])
allbaro['FPbaro']=FP['Bar']/10
allbaro['NDBCbaro']=NDBCbaro['NDBCbaro']
allbaro['TULAbaro']=TULAbaro['TULAbaro']

## Fill priority = FP,NDBC,TAFUNA,TULA
allbaro['Baropress']=allbaro['FPbaro'].where(allbaro['FPbaro']>0,allbaro['NDBCbaro']) ## create a new column and fill with FP or NDBC
allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TAFUNAbaro'])
allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TULAbaro']) 


#### Import PT Data
# ex. PT_Levelogger(allbaro,PTname,datapath,tshift=0,zshift=0): 
from load_from_MASTER_XL import PT_Hobo,PT_Levelogger

PT1 = PT_Levelogger(allbaro,'PT-Nuuuli1',XL,'PT-Nuuuli1',0,0)
PT2 = PT_Levelogger(allbaro,'PT-Nuuuli2',XL,'PT-Nuuuli2',0,0)

## STAGE DATA FOR PT's
stage_data = pd.DataFrame({'N1':PT1['stage'],'N2':PT2['stage']})

## Year Interval Times
start2012, stop2012 = dt.datetime(2012,1,7,0,0), dt.datetime(2012,12,31,11,59)    
start2013, stop2013 = dt.datetime(2013,1,1,0,0), dt.datetime(2013,12,31,11,59)
start2014, stop2014 = dt.datetime(2014,1,1,0,0), dt.datetime(2014,12,31,11,59)   
PT1 = PT1.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
PT2 = PT2.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
stage_data = stage_data.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

#### Import T and SSC Data
from load_from_MASTER_XL import OBS,loadTSS

N1_OBS = OBS(XL,sheet='N1-OBS')
N2_OBS = OBS(XL,sheet='N2-OBS')

N1_OBS = N1_OBS.rename(columns={'Turb_SS_Min':'NTU'})
N2_OBS = N2_OBS.rename(columns={'Turb_SS_Min':'NTU'})


## TSS Data, equivalent to SSC but I don't want to change all the code and file names
TSSXL = pd.ExcelFile(datadir+'SSC/TSS_grab_samples.xlsx')
TSS = loadTSS(TSSXL,'ALL_MASTER')
TSS= TSS[TSS['TSS (mg/L)']>0]


#### Import NUTRIENT Data
from load_from_MASTER_XL import loadNUTES1,loadNUTES2and3
##NUTRIENTS1 (first field season)
NUTESXL = pd.ExcelFile(datadir+'NUTRIENTS/NUTRIENTS1.xlsx')
NUTES1 = loadNUTES1(NUTESXL,'Data')
##NUTRIENTS2and3 (second and third field season)
NUTES2XL = pd.ExcelFile(datadir+'NUTRIENTS/NUTRIENTS from Lisa 5_5_14.xlsx')
NUTES2infoXL = pd.ExcelFile(datadir+'NUTRIENTS/NUTRIENTS to Lisa 3_17_14.xlsx')
NUTES2and3 = loadNUTES2and3(NUTES2XL,NUTES2infoXL)

#NUTES2and3.to_excel(datadir+'samoa/WATERSHED_ANALYSIS/NUTRIENTS/NUTES2and3.xlsx')
NUTES = NUTES1.append(NUTES2and3)
#NUTES.to_excel(datadir+'samoa/WATERSHED_ANALYSIS/NUTRIENTS/NUTES_ALL.xlsx')
