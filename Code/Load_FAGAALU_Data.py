# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 07:40:01 2014

@author: Alex
"""

#### Import modules
## Data Processing
import os
import numpy as np
import pandas as pd
#import math
import datetime as dt
import matplotlib.pyplot as plt
#import pytz
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
    
#### Import PRECIP Data
from precip_data import raingauge#, AddTimu1, AddTimu1Hourly, AddTimu1Daily, AddTimu1Monthly

print 'opening MASTER_DATA excel file...'+dt.datetime.now().strftime('%H:%M:%S')
if 'XL' not in locals():
    XL = pd.ExcelFile(datadir+'MASTER_DATA_FAGAALU.xlsx')
print 'MASTER_DATA opened: '+dt.datetime.now().strftime('%H:%M:%S')

## Timu-Fagaalu 1 (by the Quarry)
Precip = raingauge(XL,'Timu-Fagaalu1-2013',180) ## (path,sheet,shift) no header needed
Precip = Precip.append(raingauge(XL,'Timu-Fagaalu1-2014',0)) ## (path,sheet,shift) no header needed
Precip.columns=['Timu1']
Precip['Timu1-15']=Precip['Timu1'].resample('15Min',how='sum')
Precip['Timu1-30']=Precip['Timu1'].resample('30Min',how='sum')

Precip['Timu1hourly']= Precip['Timu1'].resample('H',how='sum')
Precip['Timu1hourly'].dropna().to_csv(datadir+'OUTPUT/Timu1hourly.csv',header=['Timu1hourly'])

Precip['Timu1daily'] = Precip['Timu1'].resample('D',how='sum')
Precip['Timu1daily'].dropna().to_csv(datadir+'OUTPUT/Timu1daily.csv',header=['Timu1daily'])

Precip['Timu1monthly'] = Precip['Timu1'].resample('MS',how='sum') ## Monthly Precip
Precip['Timu1monthly'].dropna().to_csv(datadir+'OUTPUT/Timu1monthly.csv',header=['Timu1monthly'])

## Timu-Fagaalu2 (up on Blunt's Point Ridge; only deployed for 2 months in 2012)
Precip['Timu2-30']=raingauge(XL,'Timu-Fagaalu2',180).resample('30Min',how='sum')

Precip['Timu2hourly']= Precip['Timu2-30'].resample('H',how='sum')
Precip['Timu2hourly'].dropna().to_csv(datadir+'OUTPUT/Timu2hourly.csv',header=['Timu2hourly'])

Precip['Timu2daily'] = Precip['Timu2-30'].resample('D',how='sum')
Precip['Timu2daily'].dropna().to_csv(datadir+'OUTPUT/Timu2daily.csv',header=['Timu2daily'])

Precip['Timu2monthly'] = Precip['Timu2-30'].resample('MS',how='sum') ## Monthly Precip
Precip['Timu2monthly'].dropna().to_csv(datadir+'OUTPUT/Timu2monthly.csv',header=['Timu2monthly'])


#### Import WX STATION Data
from load_from_MASTER_XL import WeatherStation

FPa = WeatherStation(XL,'FP-30min')
Bar15Min=FPa['Bar'].resample('15Min',fill_method='pad',limit=2) ## fill the 30min Barometric intervals to 15minute, but not Precip!
FPa = FPa.resample('15Min')
FPa['Bar']=Bar15Min
FPb = WeatherStation(XL,'FP-15min')
FP = FPa.append(FPb)

Precip['FPrain']=FP['Rain'] ## mm?
Precip['FPrain-30']=Precip['FPrain'].resample('30Min',how=sum)
Precip['FPhourly'] = Precip['FPrain'].resample('H',how='sum') ## label=left?? 
Precip['FPdaily'] = Precip['FPrain'].resample('D',how='sum')
Precip['FPmonthly'] = Precip['FPrain'].resample('MS',how='sum')

Precip['FPhourly'].dropna().to_csv(datadir+'OUTPUT/FPhourly.csv',header=['FPhourly'])
Precip['FPdaily'].dropna().to_csv(datadir+'OUTPUT/FPdaily.csv',header=['FPdaily'])
Precip['FPmonthly'].dropna().to_csv(datadir+'OUTPUT/FPmonthly.csv',header=['FPmonthly'])

## Filled Precipitation record, priority = Timu1, fill with FPrain
PrecipFilled=pd.DataFrame(pd.concat([Precip['Timu1-15'][dt.datetime(2012,1,7):dt.datetime(2013,2,8)],Precip['FPrain'][dt.datetime(2013,2,8,0,15):dt.datetime(2013,3,12)],Precip['Timu1-15'][dt.datetime(2013,3,12,0,15):dt.datetime(2013,3,24)],Precip['FPrain'][dt.datetime(2013,3,24,0,15):dt.datetime(2013,5,1)],Precip['Timu1-15'][dt.datetime(2013,5,1,0,15):dt.datetime(2014,8,5)]]),columns=['Precip']).dropna()

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


##load data from Tafuna Intl ## To get more data from the Airport run wundergrabber_NSTU.py in the 'Maindir+Data/NSTU/' folder
airport = pd.DataFrame.from_csv(datadir+'BARO/NSTU/NSTU-current.csv') ## download new data using wundergrabber
airport['Wind Speed m/s']=airport['Wind SpeedMPH'] * 0.44704
#TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea LevTim Bodellel PressureIn'] * 3.3863881579}).resample('15Min',fill_method='ffill',limit=2)## inches to kPa
TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea Level PressureIn'] *.1}).resample('15Min')## inches to kPa
TAFUNAbaro = TAFUNAbaro.reindex(pd.date_range(min(TAFUNAbaro.index),max(TAFUNAbaro.index),freq='15Min'))
TAFUNAbaro = TAFUNAbaro[TAFUNAbaro>=90.0] ## filter erroneous values
##load data from NDBC NSTP6 station at DMWR, Pago Harbor
## To get more NSTP6 data either go to their website and copy and paste the historical data
## or use wundergrabber_NSTP6-REALTIME.py and copy and paste frome the .csv
def ndbc(datafile = datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx'):
    ndbcXL = pd.ExcelFile(datafile)
    ndbc_parse = lambda yr,mo,dy,hr,mn: dt.datetime(yr,mo,dy,hr,mn)
    ndbc_data = ndbcXL.parse('NSTP6-2012-14',header=0,skiprows=1,parse_dates=[['#yr','mo','dy','hr','mn']],index_col=0,date_parser=ndbc_parse,
                             na_values=['9999','999','99','99.0'])
    #local = pytz.timezone('US/Samoa')
    #ndbc_data.index = ndbc_data.index.tz_localize(pytz.utc).tz_convert(local)
    return ndbc_data

NDBCbaro = ndbc(datafile = datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx')
NDBCbaro = NDBCbaro['hPa'].resample('15Min')
NDBCbaro = NDBCbaro.interpolate(method='linear',limit=4)
NDBCbaro.columns=['NDBCbaro']
NDBCbaro=NDBCbaro.shift(-44) ## UTC to Samoa local  =11 hours =44x15min
NDBCbaro = NDBCbaro-.025
 
##load data from NOAA Climate Observatory at Tula, East Tutuila
TULAbaro= pd.DataFrame(Tula(datadir+'BARO/TulaStation/TulaMetData/'),columns=['TULAbaro']) ## add TULA barometer data

## Build data frame of barometric data: Make column 'baropress' with best available data
allbaro = pd.DataFrame(NDBCbaro/10)
allbaro['FPbaro']=FP['Bar']/10
allbaro['NDBCbaro']=NDBCbaro/10
allbaro['TULAbaro']=TULAbaro['TULAbaro']

## Fill priority = FP,NDBC,TAFUNA,TULA
allbaro['Baropress']=allbaro['FPbaro'].where(allbaro['FPbaro']>0,allbaro['NDBCbaro']) ## create a new column and fill with FP or NDBC
#allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TAFUNAbaro'])
#allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TULAbaro']) 

#### Import PT Data
# ex. PT_Levelogger(allbaro,PTname,datapath,tshift=0,zshift=0): 
from load_from_MASTER_XL import PT_Hobo,PT_Levelogger

PT1a = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1a',12) #12 x 15min = 3hours
PT1ba = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ba',3)
PT1bb = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bb',3,zshift=-1.5)
PT1c = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1c',0)
PT1 = pd.concat([PT1a,PT1ba,PT1bb,PT1c])

PT2 = PT_Levelogger(allbaro,'PT2 Drive Thru',XL,'PT-Fagaalu2',0,-22)
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3a = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3a',12,-3.75)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',XL,'PT-Fagaalu3b',0,-23)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',XL,'PT-Fagaalu3c',0,-19.5)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',XL,'PT-Fagaalu3d',0,-17.1)

PT3e = PT_Levelogger(allbaro,'PT3e Dam',XL,'PT-Fagaalu3e',0,-18.4)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',XL,'PT-Fagaalu3f',0,-17)
PT3g = PT_Levelogger(allbaro-1.5,'PT3g Dam',XL,'PT-Fagaalu3g',0,-10.5)
PT3 = pd.concat([PT3a,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])
PT3 = PT3[PT3>0]


## Year Interval Times
start2012, stop2012 = dt.datetime(2012,1,7,0,0), dt.datetime(2012,12,31,11,59)    
start2013, stop2013 = dt.datetime(2013,1,1,0,0), dt.datetime(2013,12,31,11,59)
start2014, stop2014 = dt.datetime(2014,1,1,0,0), dt.datetime(2014,12,31,11,59)   

PT1 = PT1.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
PT3 = PT3.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

def plot_stage_data(show=False):
    fig, ax = plt.subplots()
    allbaro.plot(ax=ax)
    PT1list = [PT1a,PT1b,PT1c]
    
    for PT in PT1list:
        try:
            PT['Pressure'][PT['Pressure']>0].plot(ax=ax,c=np.random.rand(3,1))
        except KeyError:
            PT['LEVEL'][PT['LEVEL']>0].plot(ax=ax,c=np.random.rand(3,1))
        plt.legend()
        ax.set_ylim(100,120)
    if show==True:
        plt.draw()
        plt.show()
    return
#plot_stage_data(show=True)
    


#### Import FIELD NOTEBOOK Data
from notebook import FieldNotes
fieldbookdata = datadir+'FieldNotebook-dataonly.xlsx'
Timu1fieldnotes = FieldNotes('Timu-F1notes',3,fieldbookdata)

Timu1mmcheck = Timu1fieldnotes.ix[:,'mm':'to 0.1'] ##take the records from the mannual gage and if it was emptied to zero
Timu1mmcheck['mm true'] = Timu1mmcheck['mm']-Timu1mmcheck['to 0.1'].shift(1)

Timu1mmcheck['end']=Timu1mmcheck.index## add a column for time
Timu1mmcheck['start']=Timu1mmcheck['end'].shift(1) ## take the time and shift it down so you have a start and stop time: When the gauge was emptied to zero, it was the start of the next interval
Timu1mmcheck=Timu1mmcheck.truncate(before = Timu1mmcheck.index[5])
from HydrographTools import StormSums
Timu1mmcheck['Timu1 mm sum']=StormSums(Timu1mmcheck,Precip['Timu1'])['sum'] ## from 1/20/12 onward. Timu1 QC data begins 1/21/12
Timu1mmcheck['WorldsBest - Timu1'] = Timu1mmcheck['Timu1 mm sum']-Timu1mmcheck['mm']

LBJfieldnotes = FieldNotes('LBJstage',1,fieldbookdata)
LBJfieldnotesStage = pd.DataFrame(LBJfieldnotes['RefGageHeight(cm)'].resample('15Min',how='first').dropna(),columns=['RefGageHeight(cm)'])
LBJfieldnotesStage['PT1']=PT1['stage']
LBJfieldnotesStage['GH-PT']=LBJfieldnotesStage['RefGageHeight(cm)']-PT1['stage']

PT1['GH Correction']=LBJfieldnotesStage['GH-PT']
PT1['GH Correction Int']= PT1['GH Correction'].interpolate()
PT1['stage corrected'] = PT1['stage']+PT1['GH Correction Int']

## Plot Stage Correction
#PT1['stage'].plot=('y')
#LBJfieldnotesStage['RefGageHeight(cm)'].plot(ls='None',marker='o',markersize=6,c='g')
#PT1['stage corrected'].plot(color='k')


StageCorrXL = pd.ExcelFile(datadir+'Q/StageCorrection.xlsx')
def correct_Stage(StageCorrXL,location,PTdata):
    print 'Correcting stage for '+location
    StageCorr = StageCorrXL.parse(location)
    Correction=pd.DataFrame()
    for correction in StageCorr.iterrows():
        t1 = correction[1]['T1_date']
        t2 = correction[1]['T2_date']
        z = correction[1]['z']    
        print t1,t2, z
        Correction = Correction.append(pd.DataFrame({'z':z},index=pd.date_range(t1,t2,freq='15Min')))
    Correction = Correction.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    PTdata['stage_Correction'] = Correction['z']
    PTdata['stage_Corrected'] = PTdata['stage']+PTdata['stage_Correction']
    PTdata['stage']=PTdata['stage_Corrected'].where(PTdata['stage_Corrected']>0,PTdata['stage'])
    return PTdata
    
PT1 = correct_Stage(StageCorrXL,'LBJ',PT1)
PT3 = correct_Stage(StageCorrXL,'DAM',PT3)

## STAGE DATA FOR PT's
#### FINAL STAGE DATA with CORRECTIONS
Fagaalu_stage_data = pd.DataFrame({'LBJ':PT1['stage'],'DT':PT2['stage'],'Dam':PT3['stage']})

Fagaalu_stage_data = Fagaalu_stage_data.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

#### Import T and SSC Data
from load_from_MASTER_XL import TS3000,YSI,OBS,loadSSC
## Turbidimeter Data DAM
DAM_TS3K = TS3000(XL,'DAM-TS3K')
DAM_YSI = YSI(XL,'DAM-YSI')
## Correct negative NTU values
DAM_YSI['NTU'][dt.datetime(2013,6,1):dt.datetime(2013,12,31)]=DAM_YSI['NTU'][dt.datetime(2013,6,1):dt.datetime(2013,12,31)]+6

## Turbidimeter Data LBJ
LBJ_YSI = YSI(XL,'LBJ-YSI')
LBJ_OBSa = OBS(XL,'LBJ-OBSa').truncate(after=dt.datetime(2013,4,1))
LBJ_OBSb = OBS(XL,'LBJ-OBSb')
LBJ_OBSa=LBJ_OBSa.rename(columns={'Turb_SS_Avg':'FNU'})
LBJ_OBSb=LBJ_OBSb.rename(columns={'Turb_SS_Mean':'FNU'})
LBJ_OBS=LBJ_OBSa.append(LBJ_OBSb)

## SSC Data, equivalent to SSC but I don't want to change all the code and file names
SSCXL = pd.ExcelFile(datadir+'SSC/SSC_grab_samples.xlsx')
SSC = loadSSC(SSCXL,'ALL_MASTER')
SSC= SSC[SSC['SSC (mg/L)']>0]


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


